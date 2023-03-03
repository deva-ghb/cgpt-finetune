from db import dbUtil
from gpt import gptUtil

# print(dbUtil.get_summary(0))
# print(dbUtil.get_allchat(0))

txt = dbUtil.get_allchat(0)

print("original text \n\n", txt)


print("summarized text \n\n", gptUtil.summarize_text(txt))