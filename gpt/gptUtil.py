import os
from dotenv import load_dotenv
load_dotenv()
import openai


# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")



def partition_the_text(text, delimiter = ".", major_partition = 0.66):
    """
    partition the text into 2 parts,
    takes : 
        major_partition - portion that go into major partition
        delimiter - splitting criteria
    """
    sentences = text.split(delimiter)
    nSentences = len(sentences)
    p1_end = int(major_partition * nSentences)
    part1 = sentences[ : p1_end]
    part2 = sentences[p1_end : ]

    return " ".join(part1), " ".join(part2)

def summarize_as_two_parts(prompt):
    """
    split the text into 2 parts (2/3, 1/3)
    summarize each part and combine the output
    """
    part1, part2 = partition_the_text(prompt, major_partition= 0.66)

    print("part1 : \n", part1)
    print("part2 : \n", part2)

    part1_summary = summarize_text(part1)
    part2_summary = summarize_text(part2)
    return part1_summary + "\n" + part2_summary



def summarize_text(current_summary, conversation):
    print('\n\ncalling summarize..\n\n')
    augmented_prompt = f"""
    Go through the conversation between user and corporation bot along with current summary provided
    and generate new summary as whole response by giving relative preference to the conversation and then to current summary to understand the user concerns and bot responses 
    current_summary : {current_summary}
    conversation : {conversation}
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                #{"role": "system", "content": "we are talking about pineapple, particulary pineapple with blue dots.."},
                {"role": "user", "content": augmented_prompt}
            ]
    )

    content = completion["choices"][0]["message"]["content"]

    print("content\n\n", content)

    
    return content





if __name__ == '__main__':
    
    txt = """
    The beautiful sun rose above the majestic mountains, casting a warm golden glow over the serene valley below. A gentle breeze rustled the leaves of the tall trees, creating a soothing melody that filled the air. As I walked through the peaceful countryside, I couldn't help but feel grateful for the simple beauty of nature. The chirping of the birds and the buzzing of the bees were the only sounds that could be heard, and the fresh scent of wildflowers wafted through the air. It was a perfect morning, and I felt at peace with the world.
    """
    # print("original text :\n" + txt + "\n\n")
    # print("total summary :\n" + summarize_text(txt) + "\n\n")
    # print("parts summary :\n" + summarize_as_two_parts(txt) + "\n\n")
