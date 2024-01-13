from vocabulary_controller import *

# uncomment to test

#----------------------------------------------------------------------------------------

# test new documents
# name = "oldman team"
# vocabularies = [
#     {"vocabulary": "提供", "example": "この番組は、ご覧のスポンサーの提供でお送りしました"},
#     {"vocabulary": "健康", "example": "あなたの健康と成功を願っています"},
#     {"vocabulary": "規則", "example": "規則正しい生活をする"},
#     {"vocabulary": "次第", "example": "良いか悪いかは考え方次第だ"},
#     ]
# print(insert_azure_doc(name, vocabularies))

#----------------------------------------------------------------------------------------

# test search documents
# print(find_user_vocabulary_by_id("65a25e01f84352e2bf5f07e6"))

#----------------------------------------------------------------------------------------

# test update documents
# name = "oldman team 4+"
# vocabularies = [
#     {"vocabulary": "提供", "example": "この番組は、ご覧のスポンサーの提供でお送りしました"},
#     {"vocabulary": "健康", "example": "あなたの健康と成功を願っています"}, # delete three vocabulary
#     {"vocabulary": "次第", "example": "次第に減っていくでしょう？"}, # update example
#     ]
# print(update_user_by_id("65a25e01f84352e2bf5f07e6", name, vocabularies))
