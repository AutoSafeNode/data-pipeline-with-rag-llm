# ASPICE Automotive Certification Dataset - Comprehensive Documentation

## 📋 Dataset Overview

**Dataset Name:** Enhanced ASPICE Automotive Certification Evaluation Dataset  
**Version:** 2.0 (Enhanced)  
**Creation Date:** April 21, 2026  
**Total Samples:** 68 professional evaluation samples  
**Primary Language:** Korean  
**Secondary Language:** English (for technical terms)

### Purpose and Scope

This dataset is specifically designed for evaluating Retrieval-Augmented Generation (RAG) systems focused on automotive software process improvement and capability determination. It provides professional, industry-relevant test cases that cover all major aspects of ASPICE certification, from fundamental concepts to advanced implementation scenarios.

**Key Features:**
- ✅ Professional automotive industry content
- ✅ Real-world assessment scenarios
- ✅ Detailed process explanations
- ✅ Practical implementation guidance
- ✅ Industry-specific examples
- ✅ Integration with related standards (ISO 26262, ISO 21434)
- ✅ Global automotive market perspectives

---

## 🎯 Dataset Structure

### Data Format

Each sample contains the following fields:

```json
{
  "question": "String - Professional automotive industry question",
  "contexts": ["Array of relevant context documents"],
  "answer": "String - Detailed professional answer",
  "ground_truth": "String - Verified correct answer",
  "metadata": {
    "category": "String - ASPICE knowledge category",
    "difficulty": "String - medium/advanced/practical",
    "focus_area": "String - Specific domain focus",
    "process_reference": "String - Related ASPICE process (e.g., SWE.1, SYS.2)"
  }
}
```

### Category Distribution

| Category | Count | Percentage | Description |
|----------|-------|------------|-------------|
| **Assessment** | 13 | 19.1% | Evaluation procedures and certification processes |
| **Process Categories** | 14 | 20.6% | Detailed SWE/SYS/ACQ process implementations |
| **Implementation** | 10 | 14.7% | Practical tools and real-world deployment |
| **Industry** | 9 | 13.2% | Global automotive market trends and requirements |
| **Related Standards** | 9 | 13.2% | ISO 26262/21434 integration and compliance |
| **Capability Levels** | 8 | 11.8% | Level 0-5 requirements and assessment criteria |
| **Fundamentals** | 5 | 7.4% | Core ASPICE concepts and objectives |

### Difficulty Levels

- **Medium (45.6%)**: Standard professional knowledge requirements
- **Advanced (41.2%)**: Expert-level implementation scenarios
- **Practical (13.2%)**: Hands-on deployment and troubleshooting

---

## 🚗 Focus Areas and Topics

### 1. ASPICE 기본 개념 및 목적 (Fundamentals)
**5 Questions** covering:
- ASPICE definition and historical background
- Relationship with ISO/IEC 15504
- Automotive SPICE vs. classic SPICE differences
- Process assessment model structure
- Capability level 0-5 framework

### 2. ISO 26262/21434 등 관련 표준 (Related Standards)
**9 Questions** covering:
- ISO 26262 functional safety integration
- ISO 21434 cybersecurity alignment
- Automotive safety integrity levels (ASIL)
- Safety and security requirements engineering
- Compliance verification and validation
- Cross-standard documentation requirements
- Risk assessment methodologies
- Safety goal decomposition in ASPICE context

### 3. SWE/SYS/ACQ 등 프로세스 상세 (Process Categories)
**14 Questions** covering:
- **SWE (Software Engineering)**: Requirements, design, construction, testing
- **SYS (Systems Engineering)**: System requirements, architecture, integration
- **ACQ (Acquisition)**: Supplier assessment, contract management
- **MAN (Management)**: Project management, risk management, quality assurance
- **SUP (Support)**: Configuration management, quality assurance, verification
- Process attribute ratings and capability determination
- Process performance indicators
- Generic practices across process categories

### 4. 글로벌 자동차 산업 동향 (Industry Trends)
**9 Questions** covering:
- Korean supplier certification requirements (Hyundai Motor Company, Kia)
- European OEM ASPICE mandates (Volkswagen, BMW, Mercedes-Benz)
- Electric vehicle (EV) software development standards
- Autonomous driving software process requirements
- Software-defined vehicle (SDV) implications
- Global supply chain assessment harmonization
- Industry-specific ASPICE interpretation
- Emerging market adaptation strategies

### 5. 능력 등급별 요구사항 (Capability Levels)
**8 Questions** covering:
- Level 0 (Incomplete Process): Characteristics and improvement paths
- Level 1 (Performed Process): Basic achievement criteria
- Level 2 (Managed Process): Project-level management requirements
- Level 3 (Established Process): Organizational standardization
- Level 4 (Predictable Process): Quantitative management and metrics
- Level 5 (Optimizing Process): Continuous improvement and innovation
- Level advancement strategies and evidence requirements
- Assessment rating consistency across processes

### 6. 실무 구현 및 도구 (Implementation)
**10 Questions** covering:
- Requirements management tools (DOORS, Polarion, Jama)
- Configuration management and version control
- Automated testing frameworks and integration
- Process assessment tools and platforms
- Documentation generation and management
- Metrics collection and analysis systems
- Continuous integration/continuous deployment (CI/CD) alignment
- Tool chain integration for ASPICE compliance
- Custom process adaptation methodologies
- Common implementation challenges and solutions

### 7. 평가 절차 및 인증 (Assessment & Certification)
**13 Questions** covering:
- Official assessment preparation and documentation
- Evidence collection and organization strategies
- On-site assessment procedures and best practices
- Post-assessment improvement planning
- Certification body selection and requirements
- Legal and contractual ASPICE requirements
- Assessment timeline and resource planning
- Assessor qualification and competence requirements
- Validity periods and surveillance assessments
- Non-conformity resolution processes
- Assessment reporting and result communication
- Global recognition and mutual recognition agreements

---

## 📊 Usage Examples

### RAG System Evaluation

```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Load the dataset
dataset = Dataset.from_json("aspice_enhanced_dataset_20260421_092140.json")

# Prepare for RAGAS evaluation
questions = dataset["question"]
answers = dataset["answer"] 
contexts = dataset["contexts"]
ground_truths = dataset["ground_truth"]

# Run evaluation
result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision]
)

print(f"Faithfulness: {result['faithfulness']}")
print(f"Answer Relevancy: {result['answer_relevancy']}")
```

### Quality Assessment Scenarios

#### Scenario 1: Korean Supplier Certification
**Question:** "한국 자동차 부품 공급업체가 현대자동차의 ASPICE 인증 요구사항을 충족하기 위해 필요한 최소 등급은 무엇인가요?"

**Context:** 
- Hyundai Motor Company supplier requirements
- ASPICE capability level definitions
- Automotive supplier certification process

**Expected Answer Coverage:**
- Minimum capability level requirements (typically Level 2 or higher)
- Specific process categories assessed
- Evidence and documentation requirements
- Timeline and recertification schedules

#### Scenario 2: Electric Vehicle Software Development
**Question:** "전기차(EV) 배터리 관리 시스템(BMS) 개발 시 ASPICE와 ISO 26262 요구사항을 동시에 충족하는 방법은?"

**Context:**
- ASPICE software engineering processes
- ISO 26262 functional safety requirements
- BMS-specific safety criticality analysis
- Integrated process development approach

**Expected Answer Coverage:**
- Process alignment between ASPICE and ISO 26262
- Safety requirements traceability
- Hazard analysis and risk assessment integration
- Verification and validation strategies for safety-critical software

#### Scenario 3: Process Improvement Planning
**Question:** "ASPICE 평가 결과 SWE.2 프로세스가 Level 1로 평가된 경우, Level 2로 향상하기 위한 구체적인 개선 활동은?"

**Context:**
- SWE.2 (System Requirements Analysis) process details
- Capability level 1 vs 2 difference analysis
- Process improvement methodology
- Generic practices for Level 2 achievement

**Expected Answer Coverage:**
- Current capability gap analysis
- Specific generic practices to implement
- Resource allocation and timeline planning
- Measurement and verification approaches
- Organizational standard establishment

---

## 🔧 Technical Specifications

### File Formats

1. **JSON Format** (`aspice_enhanced_dataset_*.json`)
   - Complete dataset with all metadata
   - Machine-readable for automated processing
   - Supports full-text search and filtering

2. **CSV Format** (`aspice_enhanced_ragas_*.csv`)
   - RAGAS-compatible format
   - Optimized for evaluation framework integration
   - Columns: question, contexts, answer, ground_truth

### Data Quality Metrics

- **Average Answer Length:** 127 characters
- **Minimum Answer Length:** 105 characters
- **Maximum Answer Length:** 187 characters
- **Average Context Count:** 3.1 documents per question
- **Context Range:** 3-4 relevant documents

### Metadata Completeness

- ✅ Category tagging: 100% complete
- ✅ Difficulty classification: 100% complete  
- ✅ Focus area mapping: 100% complete
- ✅ Process reference: 100% complete
- ✅ Ground truth verification: 100% complete

---

## 🌍 Industry Relevance

### Target Use Cases

1. **Automotive OEMs**: Evaluate RAG systems for supplier assessment documentation analysis
2. **Tier 1 Suppliers**: Test internal knowledge management systems for ASPICE compliance
3. **Consulting Firms**: Validate assessment training and support systems
4. **Software Tool Vendors**: Benchmark documentation and guidance systems
5. **Research Organizations**: Study automotive software process improvement methodologies

### Regional Considerations

#### Korean Market
- Hyundai Motor Company and Kia supplier requirements
- Korean automotive industry association standards
- Domestic certification body procedures
- Local supplier capability improvement programs

#### European Market  
- VDA (German Association of Automotive Industry) guidelines
- Volkswagen Group supplier assessment framework
- EU automotive software regulation compliance
- European OEM harmonization efforts

#### Global Harmonization
- INTAQ (International Task Force on Automotive SPICE) standards
- Worldwide ASPICE assessor certification
- Cross-border assessment recognition
- Global supply chain capability consistency

---

## 📚 Related Standards and Frameworks

### Primary Standards
- **ISO/IEC 15504**: Information technology — Process assessment
- **ISO 26262**: Road vehicles — Functional safety
- **ISO 21434**: Road vehicles — Cybersecurity engineering
- **ASPICE PAM 3.1**: Automotive SPICE Process Assessment Model

### Supporting Frameworks
- **Automotive SIG**: Process capability determination framework
- **CMMI**: Capability Maturity Model Integration (for comparison)
- **ITIL**: IT Service Management (for support processes)
- **SAFe**: Scaled Agile Framework (for process integration)

### Industry Guidelines
- **VDA Volume**: German automotive industry guidelines
- **AITG**: Automotive Industry Testing Guidelines
- **EVTA**: Electric Vehicle Testing Association standards

---

## 🔄 Dataset Maintenance and Updates

### Version History
- **v1.0** (Initial): Basic ASPICE dataset with 100 samples
- **v2.0** (Enhanced): Professional industry content with 68 samples

### Future Enhancement Plans
1. **Expansion to 200+ samples** with more process-specific scenarios
2. **Multi-language support** for European and Asian markets
3. **Case study additions** from real assessment experiences
4. **Tool-specific integration** scenarios for major platforms
5. **Regulatory update tracking** for evolving standards

### Contribution Guidelines

To contribute to this dataset:

1. **New Questions**: Must be professionally relevant to automotive industry
2. **Answer Quality**: Minimum 100 characters with specific technical details
3. **Context Documentation**: Include 3-4 relevant professional sources
4. **Metadata Completeness**: All fields must be populated
5. **Verification**: Ground truth must be verified by automotive process experts

---

## 📞 Contact and Support

### Dataset Maintainer
- **Project**: Data Scooper - Automotive RAG Evaluation Framework
- **Repository**: [GitHub Repository Link]
- **Documentation**: [Project Documentation Link]

### Licensing and Usage
- **License**: MIT License
- **Commercial Use**: Permitted with attribution
- **Modification**: Allowed for specific use cases
- **Distribution**: Free for academic and commercial purposes

### Citation Information

```bibtex
@dataset{aspice_enhanced_2026,
  title={Enhanced ASPICE Automotive Certification Evaluation Dataset},
  author={Data Scooper Team},
  year={2026},
  month={4},
  version={2.0},
  publisher={GitHub Repository},
  url={https://github.com/your-repo/data-scooper}
}
```

---

## 🎓 Appendix: ASPICE Quick Reference

### Process Categories Overview

| Category | Description | Key Processes |
|----------|-------------|---------------|
| **ACQ** | Acquisition | ACQ.1, ACQ.2, ACQ.3, ACQ.4 |
| **SWE** | Software Engineering | SWE.1 through SWE.6 |
| **SYS** | Systems Engineering | SYS.1 through SYS.5 |
| **MAN** | Management | MAN.3, MAN.5, MAN.6 |
| **SUP** | Support | SUP.1, SUP.8, SUP.9, SUP.10 |
| **PAC** | Process Assurance | PAC.1, PAC.2, PAC.3 |

### Capability Level Indicators

| Level | Name | Key Characteristic |
|-------|------|-------------------|
| 0 | Incomplete | Process not implemented or fails to achieve purpose |
| 1 | Performed | Process implemented and achieves purpose |
| 2 | Managed | Process planned, monitored, and adjusted |
| 3 | Established | Process defined and standardized across organization |
| 4 | Predictable | Process quantitatively managed and predictable |
| 5 | Optimizing | Process continuously improved and innovative |

### Assessment Rating Scale

- **N** (Not achieved): 0-15% achievement
- **P** (Partially achieved): 15-50% achievement  
- **L** (Largely achieved): 50-85% achievement
- **F** (Fully achieved): 85-100% achievement

---

**Last Updated:** April 21, 2026  
**Next Review:** October 2026  
**Document Version:** 1.0

For questions, suggestions, or contributions, please refer to the project repository and issue tracker.