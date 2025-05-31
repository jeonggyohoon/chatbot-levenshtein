import pandas as pd
import Levenshtein  # 문자열 유사도 계산을 위한 레벤슈타인 거리 라이브러리

class LevenshteinChatBot:
    def __init__(self, file_path: str):
        """
        챗봇 초기화: 질문과 답변 데이터를 로드합니다.
        """
        self.questions, self.answers = self._load_data(file_path)

    def _load_data(self, file_path: str):
        """
        CSV 파일에서 질문과 답변 데이터를 불러옵니다.

        매개변수:
            file_path (str): CSV 파일 경로

        반환값:
            tuple: 질문 리스트와 답변 리스트
        """
        df = pd.read_csv(file_path)
        return df['Q'].tolist(), df['A'].tolist()

    def find_best_answer(self, user_input: str):
        """
        사용자 입력과 가장 유사한 질문을 찾아 해당 답변을 반환합니다.

        매개변수:
            user_input (str): 사용자가 입력한 문장

        반환값:
            tuple: (답변, 가장 유사한 질문, 레벤슈타인 거리 값)
        """
        best_score = float('inf')  # 최소 거리 초기값 설정
        best_index = -1            # 가장 유사한 질문의 인덱스

        # 모든 질문에 대해 레벤슈타인 거리 계산
        for idx, question in enumerate(self.questions):
            score = Levenshtein.distance(user_input, question)
            if score < best_score:
                best_score = score
                best_index = idx

        return self.answers[best_index], self.questions[best_index], best_score


if __name__ == '__main__':
    FILE_PATH = 'ChatbotData.csv'
    bot = LevenshteinChatBot(FILE_PATH)

    print("레벤슈타인 거리 기반 챗봇입니다. 종료하려면 '종료'를 입력하세요.\n")

    while True:
        user_input = input('You: ')
        if user_input.lower() == '종료':
            print("챗봇을 종료합니다.")
            break

        answer, matched_question, distance = bot.find_best_answer(user_input)

        print(f'\n[가장 유사한 질문] {matched_question}')
        print(f'[레벤슈타인 거리] {distance}')
        print(f'Chatbot: {answer}\n')