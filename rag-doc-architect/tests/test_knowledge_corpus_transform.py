import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


class KnowledgeCorpusTransformTest(unittest.TestCase):
    def test_builds_semantic_level_three_chunks(self):
        from convert_word_folder_to_rag_knowledge_md import build_knowledge_markdown

        lines = [
            "1、《任职资格点评-产品经理》20251224_原文",
            "2026年04月07日 09:32",
            "发言人   00:00",
            "产品经理要围绕IPD流程，从需求管理、项目管理到里程碑DCP控制，把职责补齐。",
            "发言人   01:00",
            "GTM这里不能写成主责，GTM经理负主责，产品经理负责推动和协同。",
            "发言人   02:00",
            "知识技能不能写泛，要写IPD流程、项目管理、需求管理这些具体知识。",
        ]

        markdown = build_knowledge_markdown(
            source_name="1、《任职资格点评-产品经理》20251224_原文.docx",
            source_path=r"C:\fake\1、《任职资格点评-产品经理》20251224_原文.docx",
            source_format="docx",
            role_name="产品经理",
            lines=lines,
        )

        self.assertIn('chunk_standard: "以三级标题 ### 作为向量切片边界"', markdown)
        self.assertIn("### 产品经理｜职责边界与流程接口", markdown)
        self.assertIn("### 产品经理｜知识技能与工具方法", markdown)
        self.assertIn("- 结构化要点：", markdown)
        self.assertIn("- 原话依据：", markdown)
        self.assertIn("- 可检索问题：", markdown)
        self.assertNotIn("### 发言人", markdown)


if __name__ == "__main__":
    unittest.main()
