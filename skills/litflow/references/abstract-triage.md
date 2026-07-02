# Abstract Triage — 决策参考

## 分诊流程

```
PDF → 提取摘要+元数据 → 分类(type+field) → 选择模板变体 → 精读
```

## Type 信号词速查

### research（研究论文）
- 信号词：We report, We demonstrate, We develop, Here we show, Aiming at
- 结构特征：Introduction → Results → Discussion → Methods
- 典型期刊：JACS, Nature, Science, Joule, ACS Energy Lett, Angew Chem

### review（综述）
- 信号词：Recent advances, Progress, Overview, Perspective, Survey, Tutorial
- 结构特征：无 Methods，大量引用（>100 refs），分主题章节
- 典型期刊：Chem Rev, Chem Soc Rev, Mater Today, Nat Rev Mater

### theory（理论论文）
- 信号词：We derive, We formulate, Analytical solution, Mathematical framework
- 结构特征：大量方程，Model/Analysis 章节，与数值/实验对照
- 典型期刊：J Chem Phys, Phys Rev Lett

### perspective（观点/展望）
- 信号词：Outlook, Challenges, Opportunities, Future directions, Personal view
- 结构特征：短（3-8页），引用少（30-60 refs），图少但精
- 典型期刊：Joule (Perspective), Nat Energy (Comment)

### method（方法论文）
- 信号词：We introduce, Protocol, Benchmark, Validation, Step-by-step
- 结构特征：详细的实验/计算步骤，与其他方法的对比表
- 典型期刊：Nat Methods, Anal Chem

## Field 信号词速查

### electrochemistry
- 关键词：battery, electrode, electrolyte, cycling, CV, EIS, overpotential, mAh/g
- 关注指标：容量、电压、CE、倍率、循环寿命、阻抗

### computation
- 关键词：DFT, MD, ab initio, functional, basis set, convergence
- 关注指标：eV, kcal/mol, RMSE, R², 计算成本

### synthesis
- 关键词：yield, selectivity, catalyst, solvent, temperature, substrate
- 关注指标：产率、ee值、TON/TOF、底物范围

### materials
- 关键词：conductivity, morphology, XRD, SEM, TEM, stability, bandgap
- 关注指标：电导率、带隙、比表面积、稳定性

### biology
- 关键词：IC₅₀, knockout, knockdown, p-value, n=, control, assay
- 关注指标：效力、选择性、统计显著性、重复次数

## 常见分类边界

| 情况 | 处理 |
|------|------|
| 综述里有大量原创分析 | type=review, 但标记含原创见解 |
| 研究论文里有理论推导 | type=research, 加"理论模型"子节 |
| 方法论文有 benchmark 实验 | type=method, 加"实验验证"子节 |
| 不确定类型 | 默认 type=research，注释"待确认" |

## 批量分诊效率提示

- 只需读摘要+首页，不需要读全文
- 每篇分诊 < 30 秒
- 批量分诊完再统一处理，避免中途切换模板


