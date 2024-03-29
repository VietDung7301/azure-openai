from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

school_examples = [
    {
        "question": "担任",
        "answer": """
            担任 - homeroom teacher
            1. 担任は、生徒たちの第二の親です。でも、家事はしないので安心してください。
            2. 担任は、生徒の成績や悩みを管理する責任があります。でも、彼らの心の中までは読めませんよ。
            3. 担任は、学校生活での指導やサポートを提供します。でも、彼らも時々休みたいと思っています。
            4. 担任は、保護者との連絡を取ります。でも、忙しいので返信が遅れることもあります。
            5. 担任は、クラスのまとめ役です。でも、彼らも時々混乱することがあります。
""",
    },
    {
        "question": "数学",
        "answer": """
            数学 - Mathematics
            1. 数学は、数や式を扱う学問分野です。
            2. 代数、幾何学、解析学など、数学にはさまざまな分野があります。
            3. 方程式の解を求めるために数学は使われます。
            4. 数学は科学や工学、経済学など多くの分野で応用されます。
            5. 数学の原理や法則は、自然界のさまざまな現象を説明するのに役立ちます。
""",
    },
]
examples = [
    {
        "vocab": "人工知能",
        "mean": "artificial intelligence",
        "answer": """
            人工知能 - artificial intelligence

            1. 人工知能は、機械が人間のように知識を学習し、問題を解決する能力を指します。
            2. 多くの産業で、人工知能が業務の効率化や自動化を実現しています。
            3. 人工知能は、自然言語処理や画像認識などの技術に基づいています。
            4. 人工知能は、将来的には医療や交通、ロボット工学などの分野でさらなる進化が期待されています。
            5. 人工知能は、人間の能力を補完し、新たな問題解決の手段を提供することができます。
""",
    },
    {
        "vocab": "アクセス",
        "mean": "access",
        "answer": """
            アクセス - access

            1. このウェブサイトへのアクセスは、無料で利用できます。
            2. 会議室へのアクセスは、エレベーターを使って3階に行くことができます。
            3. インターネットを通じて、世界中の情報に簡単にアクセスできます。
            4. この施設は、車や公共交通機関で簡単にアクセスできる便利な場所にあります。
            5. アカウントにログインすると、プライベートなデータにアクセスすることができます。
""",
    },
#     {
#         "vocab": "access",
#         "mean": "Truy cập",
#         "answer": """
#             access - Truy cập
#             1. Access to this website is free for all, Explore its contents, have a ball!
#             2. To access the meeting room, take the elevator, On the third floor, it'll be a creator.
#             3. Through the internet, access information wide, Connect with the world, with just a slide.
#             4. This facility is conveniently accessible, By car or public transport, it's commendable.
#             5. Login to your account for private data's embrace, Access granted, your personal space.
# """,
#     },
    {
        "vocab": "担任",
        "mean": "homeroom teacher",
        "answer": """
            担任 - homeroom teacher
            1. 担任は、生徒たちの第二の親です。でも、家事はしないので安心してください。
            2. 担任は、生徒の成績や悩みを管理する責任があります。でも、彼らの心の中までは読めませんよ。
            3. 担任は、学校生活での指導やサポートを提供します。でも、彼らも時々休みたいと思っています。
            4. 担任は、保護者との連絡を取ります。でも、忙しいので返信が遅れることもあります。
            5. 担任は、クラスのまとめ役です。でも、彼らも時々混乱することがあります。
""",
    },
    {
        "vocab": "数学",
        "mean": "Mathematics",
        "answer": """
            数学 - Mathematics
            1. 数学は、数や式を扱う学問分野です。
            2. 代数、幾何学、解析学など、数学にはさまざまな分野があります。
            3. 方程式の解を求めるために数学は使われます。
            4. 数学は科学や工学、経済学など多くの分野で応用されます。
            5. 数学の原理や法則は、自然界のさまざまな現象を説明するのに役立ちます。
""",
    },
]

example_prompt = PromptTemplate(
    input_variables=["vocab", "mean", "answer"],
    template="Question: {vocab} - {mean}\n{answer}",
)

example_few_shot_prompt = FewShotPromptTemplate(
    # prefix= """The assistant is typically sarcastic and witty, producing
    # creative  and funny responses to the users questions. Here are some
    # examples:""",
    prefix="Give me some examples of vocabulary in Japanese. Here is some examples:",
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {vocab} - {mean}",
    input_variables=["vocab", "mean"],
)

explain_prompt = PromptTemplate(
    input_variables=["vocab", "mean", "language"],
    template="Explanation of '{vocab}' with mean '{mean}' in Japanese. Write in {language}",
)


def create_conversation(question, prompt_template):
    prompt = prompt_template.format(**question)
    return [
        SystemMessage(
            content="""
    The assistant is typically sarcastic and witty, producing
    creative  and funny responses to the users questions. Here are some
    examples:
"""
# content="""
# You are an assistant supporting Japanese learning.
# You have 2 types of missions:
# First, take a word, its meaning and field of use in Japanese and give 5 examples of how the word is used in this field.
# Second, describe the meaning of the word in other languages.
# You only need to do one of the 2 tasks according to my next instructions.
# """
        ),
        HumanMessage(content=prompt),
    ]
    
def create_conversation2(question, prompt_template):
    prompt = prompt_template.format(**question)
    return [
        SystemMessage(
            content="""
You are an assistant supporting Japanese learning.
Your task is take a word, its meaning and describe the meaning of the word in other languages.
"""),
        HumanMessage(content=prompt),
    ]


if __name__ == "__main__":
    # prompt = example_few_shot_prompt.format(**{"vocab": "緑", "mean": "green"})
    # print(prompt)

    # conversation = create_conversation(
    #     {"vocab": "緑", "mean": "green"}, example_few_shot_prompt
    # )
    # print(conversation)
    
    prompt = explain_prompt.format(**{"vocab": "緑", "mean": "green", "language": "Japanese"})
    print(prompt)
