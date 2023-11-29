import gradio as gr
from llm_chat import generate_response
from game_utils import *
import json

# load challenges
with open('challenges.json','r') as f:
    challenges = json.load(f)

# 功能函数
def get_problem(challenge_idx, problem_idx):
    problems = challenges[challenge_idx]['problems']
    return problems[problem_idx]

def update_challenge_info(current_chapter_index, current_challenge_index):
    return get_problem(current_chapter_index, current_challenge_index)["description"]


def update_question_info(current_chapter_index, current_challenge_index):
    global challenges
    current_chapter = challenges[current_chapter_index]
    challenge = get_problem(current_chapter_index, current_challenge_index)
    question_info = f"""\n<center><font size=4>{current_chapter["name"]}</center>\n\n <center><font size=3>{challenge["title"]}</center>"""
    return question_info


def validate_challenge(response, input, state):
    print('in validate_challenge')
    assert 'current_chapter_index' in state, 'current_chapter_index not found in state'
    assert 'current_challenge_index' in state, 'current_challenge_index not found in state'
    current_chapter_index = state['current_chapter_index']
    current_challenge_index = state['current_challenge_index']
    # 获取当前章节
    current_chapter = challenges[current_chapter_index]
    # 获取当前挑战
    challenge = current_chapter["problems"][current_challenge_index]

    foo = eval(challenge["validator"])
    if foo(response, input):
        challenge_result = "挑战成功！进入下一关。"
        # 检查是否还有更多挑战在当前章节
        if current_challenge_index < len(current_chapter["problems"]) - 1:
            # 移动到当前章节的下一个挑战
            current_challenge_index += 1
        else:
            # 如果当前章节的挑战已经完成，移动到下一个章节
            current_challenge_index = 0
            if current_chapter_index < len(challenges) - 1:
                current_chapter_index += 1
            else:
                challenge_result = "所有挑战完成！"
    else:
        challenge_result = "挑战失败，请再试一次。"
    state['current_chapter_index'] = current_chapter_index
    state['current_challenge_index'] = current_challenge_index
    print('update state: ', state)

    return challenge_result, \
        update_question_info(current_chapter_index, current_challenge_index), \
        update_challenge_info(current_chapter_index, current_challenge_index)


# gradio反馈函数
def on_submit(input, state):
    response = generate_response(input)
    history = [(input, response)]
    print(history)
    challenge_result, question_info, challenge_info = validate_challenge(response, input, state)
    print('validate_challenge done')
    return challenge_result, history, question_info, challenge_info


def jump_chapter(selected_chapter, state):
    state['current_chapter_index'] = int(selected_chapter) - 1
    state['current_challenge_index'] = 0

    current_chapter_index = state['current_chapter_index']
    current_challenge_index = state['current_challenge_index']
    # 获取当前章节
    current_chapter = challenges[current_chapter_index]
    # 获取当前挑战
    challenge = current_chapter["problems"][current_challenge_index]
    return update_question_info(current_chapter_index, current_challenge_index), \
        update_challenge_info(current_chapter_index, current_challenge_index)


# Gradio界面构建
block = gr.Blocks()

with block as demo:
    state = gr.State(dict(current_challenge_index=0,
                          current_chapter_index=0))
    current_chapter_index = 0
    current_challenge_index = 0
    gr.Markdown("""<center><font size=6>完蛋！我被LLM包围了！</center>""")
    gr.Markdown("""<font size=3>欢迎来玩LLM Riddles复刻版的复刻版，[感谢 Haoqiang Fan 的原始创意和题目](https://zhuanlan.zhihu.com/p/665393240)：完蛋！我被LLM包围了！以及[LLMRiddles的huggingface项目](https://huggingface.co/spaces/LLMRiddles/LLMRiddles):完蛋！我被LLM包围了！

你将通过本游戏对大型语言模型产生更深刻的理解。

在本游戏中，你需要构造一个提给一个大型语言模型的问题，使得它回复的答案符合要求。""")
    question_info = gr.Markdown(update_question_info(current_chapter_index, current_challenge_index))
    challenge_info = gr.Textbox(value=update_challenge_info(current_chapter_index, current_challenge_index),
                                label="当前挑战", disabled=True)
    challenge_result = gr.Textbox(label="挑战结果", disabled=True)
    chatbot = gr.Chatbot(lines=8, label='Yiyan', elem_classes="control-height")
    message = gr.Textbox(lines=2, label='输入')

    with gr.Row():
        submit = gr.Button("🚀 发送")

    selected_chapter = gr.Dropdown(label='选择章节', choices=list(range(1, len(challenges) + 1)), value='1',
                                   interactive=True)
    jump_btn = gr.Button(value="跳转章节")

    submit.click(on_submit, inputs=[message, state], outputs=[challenge_result, chatbot, question_info, challenge_info])
    jump_btn.click(jump_chapter, inputs=[selected_chapter, state], outputs=[question_info, challenge_info])

demo.queue(concurrency_count=10).launch(height=800, share=False)
