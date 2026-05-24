from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from convert_word_folder_to_rag_md import (
    detect_word_content_type,
    derive_role_name,
    extract_doc_lines,
    extract_docx_lines,
    extract_rtf_lines,
    sanitize_filename,
)


DATE_LINE_RE = re.compile(r"^\d{4}年\d{2}月\d{2}日(?:\s+\d{2}:\d{2})?$")
SPEAKER_LINE_RE = re.compile(r"^(?:发言人|说话人|Speaker)\s+\d{2}:\d{2}$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])\s*")


@dataclass(frozen=True)
class Evidence:
    anchor: str
    text: str


@dataclass(frozen=True)
class SectionRule:
    name: str
    knowledge_type: str
    keywords: tuple[str, ...]
    retrieval_questions: tuple[str, ...]


SECTION_RULES: tuple[SectionRule, ...] = (
    SectionRule(
        name="总体判断与评分结论",
        knowledge_type="总体判断",
        keywords=("总体", "整体", "标杆", "完美", "不合格", "评分", "认证", "祝贺", "最高分", "给70分", "给85分", "给90分", "给97分"),
        retrieval_questions=("这个岗位点评的总体评价是什么？", "这个岗位最终给了多少分或什么结论？"),
    ),
    SectionRule(
        name="职位定位与设置目的",
        knowledge_type="职位定位",
        keywords=("职位设置目的", "定位", "这个职位", "总负责人", "岗位", "主导责任", "使命", "核心价值"),
        retrieval_questions=("这个岗位的定位是什么？", "这个岗位的设置目的应该怎么写？"),
    ),
    SectionRule(
        name="组织关系与八爪鱼图",
        knowledge_type="组织关系",
        keywords=("八爪鱼", "右上角", "右下角", "上级", "下级", "直接下级", "虚线", "拉通", "转岗", "通道", "社招", "可以去做", "做不了"),
        retrieval_questions=("这个岗位在八爪鱼图里应该怎么放？", "这个岗位的上下游关系和发展通道是什么？"),
    ),
    SectionRule(
        name="职责边界与流程接口",
        knowledge_type="职责边界",
        keywords=(
            "职责",
            "主责",
            "负主责",
            "协助",
            "负责",
            "边界",
            "接口",
            "流程",
            "IPD",
            "GTM",
            "OTD",
            "LTC",
            "ITR",
            "MM",
            "DSTE",
            "SDM",
            "PBC",
            "GSA",
            "1-N",
            "一到N",
            "里程碑",
            "DCP",
        ),
        retrieval_questions=("这个岗位的职责边界是什么？", "这个岗位要对接哪些流程和接口？"),
    ),
    SectionRule(
        name="知识技能与工具方法",
        knowledge_type="知识技能",
        keywords=(
            "知识",
            "技能",
            "工具",
            "方法论",
            "模型",
            "了解",
            "掌握",
            "精通",
            "项目管理",
            "数据",
            "AI",
            "系统",
            "用户画像",
            "美学",
            "预测",
            "库存",
            "指标体系",
        ),
        retrieval_questions=("这个岗位需要哪些知识技能？", "这个岗位的知识技能不能写泛时应具体写哪些内容？"),
    ),
    SectionRule(
        name="素质能力与行为标准",
        knowledge_type="素质行为",
        keywords=(
            "素质",
            "行为",
            "能力",
            "主动性",
            "诚信",
            "创新",
            "服务精神",
            "影响力",
            "团队",
            "领导",
            "成就导向",
            "坚韧",
            "灵活性",
            "培养",
            "人才",
            "选育用留",
        ),
        retrieval_questions=("这个岗位需要哪些素质能力？", "这个岗位的行为标准应该体现哪些证据？"),
    ),
    SectionRule(
        name="结果指标与评价证据",
        knowledge_type="评价证据",
        keywords=(
            "指标",
            "目标",
            "达成",
            "达成率",
            "多少",
            "点击",
            "粉丝",
            "完播率",
            "库存周转率",
            "发货率",
            "错货率",
            "降本",
            "销售转化",
            "声量",
            "数量",
            "效率",
            "比例",
            "%",
            "率",
        ),
        retrieval_questions=("这个岗位评价时应该看哪些结果指标？", "原文提到了哪些可量化评价证据？"),
    ),
    SectionRule(
        name="修改建议与扣分点",
        knowledge_type="修订建议",
        keywords=(
            "要改",
            "改一改",
            "漏",
            "缺",
            "不要",
            "不用",
            "不是",
            "不应该",
            "错",
            "问题",
            "单薄",
            "泛",
            "低了",
            "补",
            "去掉",
            "删",
            "提高",
            "不必要",
            "承接感差",
            "不紧扣",
        ),
        retrieval_questions=("这个岗位文档哪里需要修改？", "这个岗位点评中指出了哪些扣分点或风险点？"),
    ),
)

FALLBACK_RULE = SectionRule(
    name="补充原话证据",
    knowledge_type="补充证据",
    keywords=(),
    retrieval_questions=("这个岗位还有哪些补充点评原话？", "原文中还有哪些可作为知识库证据的表述？"),
)


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_text(text: str) -> str:
    text = "".join(ch for ch in text if ch == "\t" or ord(ch) >= 32)
    text = text.replace("\xa0", " ").replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    text = normalize_text(text)
    if not text:
        return []
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    refined: list[str] = []
    for part in parts:
        if len(part) <= 220:
            refined.append(part)
            continue
        chunks = [chunk.strip(" ，,") for chunk in re.split(r"[，,]\s*", part) if chunk.strip()]
        refined.extend(chunk for chunk in chunks if chunk)
    return refined


def extract_meta_and_evidence(lines: list[str]) -> tuple[str | None, str | None, list[Evidence]]:
    raw_title: str | None = None
    doc_date: str | None = None
    current_anchor = "原文"
    evidence: list[Evidence] = []

    for line in lines:
        line = normalize_text(line)
        if not line:
            continue
        if raw_title is None and not DATE_LINE_RE.match(line) and not SPEAKER_LINE_RE.match(line):
            raw_title = line
            continue
        if doc_date is None and DATE_LINE_RE.match(line):
            doc_date = line
            continue
        if SPEAKER_LINE_RE.match(line):
            current_anchor = line.replace("   ", " ")
            continue
        for sentence in split_sentences(line):
            evidence.append(Evidence(current_anchor, sentence))

    return raw_title, doc_date, evidence


def taxonomy_for_role(role_name: str) -> tuple[str, str]:
    if any(word in role_name for word in ("HRBP", "人才发展", "TD")):
        return "组织与数字化", "人力资源HR"
    if "FBP" in role_name:
        return "财经与法务", "财务分析"
    if "战略" in role_name:
        return "DSTE战略管理", "战略规划"
    if any(word in role_name for word in ("供开", "交付", "PMC", "库流")):
        return "SCBG供应链", "OTD交付"
    if any(word in role_name for word in ("产品市场", "品牌", "视觉", "内容")):
        return "品牌与营销", "市场洞察MM"
    if any(word in role_name for word in ("CBU", "客户成功")):
        return "CBG电商运营", "客体VOC"
    if any(word in role_name for word in ("产品经理", "PBU", "开发")):
        return "PBG产品研发", "IPD流程"
    return "组织与数字化", "培训资料"


def title_for_role(role_name: str) -> str:
    l1, _ = taxonomy_for_role(role_name)
    return f"2026-{l1}-任职资格点评-{role_name}"


def score_evidence(text: str, rule: SectionRule) -> int:
    upper_text = text.upper()
    return sum(1 for keyword in rule.keywords if keyword.upper() in upper_text)


def classify_evidence(items: list[Evidence]) -> dict[str, list[Evidence]]:
    grouped: dict[str, list[Evidence]] = defaultdict(list)

    for item in items:
        scores = [(rule.name, score_evidence(item.text, rule)) for rule in SECTION_RULES]
        scores = [(name, score) for name, score in scores if score > 0]
        if not scores:
            grouped[FALLBACK_RULE.name].append(item)
            continue

        scores.sort(key=lambda pair: pair[1], reverse=True)
        grouped[scores[0][0]].append(item)

        important_secondary = {"修改建议与扣分点", "结果指标与评价证据"}
        for name, score in scores[1:]:
            if name in important_secondary and score >= 1:
                grouped[name].append(item)

    return grouped


def dedupe_evidence(items: Iterable[Evidence]) -> list[Evidence]:
    seen: set[tuple[str, str]] = set()
    result: list[Evidence] = []
    for item in items:
        key = (item.anchor, item.text)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def point_from_evidence(text: str) -> str:
    text = normalize_text(text)
    text = re.sub(r"^(好|好的|你看|来看|然后|这个|那|所以)[，,。 ]*", "", text)
    return text


def keyword_summary(items: list[Evidence], rule: SectionRule) -> list[str]:
    found: list[str] = []
    for keyword in rule.keywords:
        if any(keyword.upper() in item.text.upper() for item in items):
            found.append(keyword)
    return found[:8]


def render_section(role_name: str, rule: SectionRule, evidences: list[Evidence]) -> list[str]:
    evidences = dedupe_evidence(evidences)
    lines = [
        f"### {role_name}｜{rule.name}",
        "",
        f"- 适用岗位：{role_name}",
        f"- 知识类型：{rule.knowledge_type}",
    ]

    keywords = keyword_summary(evidences, rule)
    if keywords:
        lines.append(f"- 检索关键词：{'、'.join(keywords)}")

    lines.append("- 结构化要点：")
    for item in evidences[:10]:
        lines.append(f"  - {point_from_evidence(item.text)}")

    lines.append("- 原话依据：")
    for item in evidences:
        anchor = item.anchor if item.anchor else "原文"
        lines.append(f"  - [{anchor}] {item.text}")

    lines.append("- 可检索问题：")
    for question in rule.retrieval_questions:
        lines.append(f"  - {role_name}：{question}")
    lines.append("")
    return lines


def render_gsa_section(role_name: str) -> list[str]:
    return [
        f"### {role_name}｜GSA结构化解析与语料用途",
        "",
        f"- 适用岗位：{role_name}",
        "- 知识类型：GSA结构化解析",
        "- 结构化要点：",
        f"  - G（目标）：把“{role_name}”任职资格点评中的岗位定位、职责边界、任职资格、行为标准和修订建议拆成可检索知识点。",
        "  - S（策略）：不按发言时间切片，改按业务主题切片；每个三级标题单独承载一个可向量检索的主题。",
        "  - A（行动）：每个切片同时保留结构化要点、原话依据和可检索问题，便于知识库召回后追溯原文。",
        "- 原话依据：",
        "  - 本切片为知识库处理说明，不替代原文证据；具体证据见后续各主题切片。",
        "- 可检索问题：",
        f"  - {role_name} 这份任职资格点评语料应该如何切片？",
        f"  - {role_name} 这份文档为什么不按发言时间切片？",
        "",
    ]


def build_knowledge_markdown(
    source_name: str,
    source_path: str,
    source_format: str,
    role_name: str,
    lines: list[str],
) -> str:
    raw_title, doc_date, evidences = extract_meta_and_evidence(lines)
    grouped = classify_evidence(evidences)
    l1, l2 = taxonomy_for_role(role_name)
    title = title_for_role(role_name)

    output = [
        "---",
        f"title: {yaml_quote(title)}",
        f"source_file: {yaml_quote(source_name)}",
        f"source_path: {yaml_quote(source_path)}",
        f"source_format: {yaml_quote(source_format)}",
        'doc_type: "任职资格点评"',
        f"role: {yaml_quote(role_name)}",
        f"taxonomy_l1: {yaml_quote(l1)}",
        f"taxonomy_l2: {yaml_quote(l2)}",
        'chunk_standard: "以三级标题 ### 作为向量切片边界"',
        'topology: "流式文本-语义主题重组"',
        "tags:",
        f"  - {yaml_quote(l1)}",
        f"  - {yaml_quote(l2)}",
        '  - "任职资格点评"',
        f"  - {yaml_quote(role_name)}",
        '  - "知识库语料"',
        "rag_optimized: true",
        "---",
        "",
        f"## 任职资格点评知识库条目：{role_name}",
        "",
    ]

    if raw_title or doc_date:
        output.extend(
            [
                f"### {role_name}｜来源信息与文档边界",
                "",
                f"- 适用岗位：{role_name}",
                "- 知识类型：来源信息",
                "- 结构化要点：",
            ]
        )
        if raw_title:
            output.append(f"  - 原始标题：{raw_title}")
        if doc_date:
            output.append(f"  - 原始日期：{doc_date}")
        output.extend(
            [
                f"  - 原始文件：{source_name}",
                "- 原话依据：",
            ]
        )
        if raw_title:
            output.append(f"  - [原始标题] {raw_title}")
        if doc_date:
            output.append(f"  - [原始日期] {doc_date}")
        output.extend(
            [
                "- 可检索问题：",
                f"  - {role_name} 这份任职资格点评来自哪个原始文件？",
                f"  - {role_name} 这份任职资格点评的原始日期是什么？",
                "",
            ]
        )

    output.extend(render_gsa_section(role_name))

    for rule in SECTION_RULES:
        evidences_for_rule = grouped.get(rule.name, [])
        if evidences_for_rule:
            output.extend(render_section(role_name, rule, evidences_for_rule))

    fallback_evidence = grouped.get(FALLBACK_RULE.name, [])
    if fallback_evidence:
        output.extend(render_section(role_name, FALLBACK_RULE, fallback_evidence))

    output.append(f"### {role_name}｜RAG智能索引层")
    output.extend(
        [
            "",
            f"- 适用岗位：{role_name}",
            "- 知识类型：检索索引",
            "- 结构化要点：",
            f"  - 本文档已按三级标题为“{role_name}”建立主题切片。",
            "  - 检索时优先使用“岗位名 + 职责/流程/知识技能/行为标准/修改建议/评分结论”等组合问题。",
            "- 原话依据：",
            "  - 具体原话依据已分布在各主题切片中。",
            "- 可检索问题：",
        ]
    )
    for rule in SECTION_RULES[:6]:
        output.append(f"  - {role_name}：{rule.retrieval_questions[0]}")
    output.append("")

    return "\n".join(output).rstrip() + "\n"


def extract_lines_for_word(path: Path) -> tuple[str, list[str]]:
    content_type = detect_word_content_type(path)
    if content_type == "docx":
        return content_type, extract_docx_lines(path)
    if content_type == "doc":
        return content_type, extract_doc_lines(path)
    if content_type == "rtf":
        return content_type, extract_rtf_lines(path)
    raise ValueError(f"暂不支持的文档内部格式：{content_type}")


def collect_source_files(input_dir: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in input_dir.iterdir()
            if path.is_file() and path.suffix.lower() in {".doc", ".docx"} and not path.name.startswith("~$")
        ],
        key=lambda item: item.name,
    )


def convert_file(path: Path, output_dir: Path) -> Path:
    role_name = derive_role_name(path.name)
    source_format, lines = extract_lines_for_word(path)
    markdown = build_knowledge_markdown(
        source_name=path.name,
        source_path=str(path),
        source_format=source_format,
        role_name=role_name,
        lines=lines,
    )
    title = title_for_role(role_name)
    output_path = output_dir / f"{sanitize_filename(title)}.md"
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="将 Word 文档批量转成三级标题切片的 RAG 知识库语料。")
    parser.add_argument("input_dir", help="待转换 Word 文档所在目录")
    parser.add_argument("--output-dir", help="输出目录，默认写入输入目录下的“严格知识库语料版”")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else input_dir / "严格知识库语料版"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_source_files(input_dir)
    print(f"找到 {len(files)} 份 Word 文档，输出目录：{output_dir}")

    failed: list[tuple[str, str]] = []
    for path in files:
        try:
            output_path = convert_file(path, output_dir)
            print(f"[成功] {path.name} -> {output_path.name}")
        except Exception as exc:
            failed.append((path.name, str(exc)))
            print(f"[失败] {path.name}: {exc}")

    print("")
    print(f"转换完成：成功 {len(files) - len(failed)} 份，失败 {len(failed)} 份。")
    if failed:
        for name, reason in failed:
            print(f"- {name}: {reason}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
