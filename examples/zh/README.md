# 示例 · 小张（虚构）

一个完整走查：从两轮口述到账本、规则、通用版、定向版、盲投版、作品集和面试备答。人物、公司、数字全部虚构，用于演示方法。

## 看什么

| 文件 | 看点 |
| --- | --- |
| `ledger/transcripts/2026-10-01.md` | 第一轮口述里埋了 3 处常见错误：团队人数把协作算成汇报、"准确率"与"命中率"混用、试点说成上线，外加两处相对值与绝对值不分 |
| `ledger/transcripts/2026-10-03.md` | 冲突检查怎么问、用户怎么改口、改口怎么落到账本行 |
| `ledger/facts.md` | 22 行账本：每行有口径、禁用写法、来源、范围、状态 |
| `rules.md` | 红线词、禁用写法、允许写法、脱敏替换四段，脚本按标题读 |
| `jd/aipm.md` → `interview/aipm-hitmap.md` → `content/aipm-targeted.md` | JD 命中表先于定向版；"协调研发"一项如实写"支持"，缺口不用文案填 |
| `content/portfolio-kb-qa.md` | 作品集：口径与简历独立，但数字仍要在账本里（scope portfolio）。第三轮口述就是因为作品集校验抓出两个未登记数字 |
| `checks.txt` | 四份内容各跑一次 `check.py` 的实际输出 |
| `registry.md` | 四个版本的登记 |

## 自己跑一遍

```bash
S=<skill path>/scripts
python $S/check.py content/aipm-targeted.md        # 需要 Chrome；加 --no-pdf 只出 html
python $S/derive.py content/aipm-targeted.md       # 派生盲投版
```

把 `content/general.md` 里的 95% 改成 96% 再跑，看对账怎么报；把"试点"改成"已上线"，看禁用写法怎么命中。
