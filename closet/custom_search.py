import re
import requests
import json
import markdown2
from django.conf import settings
from django.contrib.auth import get_user_model

def get_first_custom_search_image_info(query, user=None):
    """
    Google Custom Search API를 이용해 이미지 검색을 수행합니다.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    # 기본 검색어에 제외할 키워드 추가
    exclude_terms = '-키즈 -주니어 -아동 -유아 -아기 -키즈라인'
    
    # CustomUser 모델에서 성별 정보 확인
    CustomUser = get_user_model()
    # print(f"[Debug] User: {user}")
    if user and isinstance(user, CustomUser) and user.gender:
        if user.gender == 'F':
            query = f'"무신사 스탠다드" "여성" {query} {exclude_terms}'
        elif user.gender == 'M':
            query = f'"무신사 스탠다드" {query} {exclude_terms}'
        else:
            query = f'"무신사 스탠다드" {query} {exclude_terms}'
    else:
        query = f'"무신사 스탠다드" {query} {exclude_terms}'

    # 디버그: 최종 검색 쿼리 출력
    # print(f"[Debug] Search Query: {query}")

    params = {
        'key': settings.GOOGLE_SEARCH_API_KEY,
        'cx': settings.GOOGLE_CSE_ID,
        'q': query,
        'searchType': 'image',
        'num': 5,
        'siteSearch': 'musinsa.com',
        'siteSearchFilter': 'i',  # only search this site
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            # 우선적으로 '/app/goods/'가 포함된 페이지 URL을 가진 결과를 선택합니다.
            for item in data['items']:
                page_link = item.get('image', {}).get('contextLink')
                if page_link and "/app/goods/" in page_link:
                    image_url = item.get('link')
                    # print(f"[Debug] Found product - Page: {page_link}")
                    # print(f"[Debug] Found product - Image: {image_url}")
                    return page_link, image_url
            # 조건에 맞는 결과가 없으면 첫 번째 결과 사용
            item = data['items'][0]
            image_url = item.get('link')
            page_link = item.get('image', {}).get('contextLink')
            print(f"[Debug] Using fallback product - Page: {page_link}")
            return page_link, image_url
    except Exception as e:
        print(f"[Debug] Error in search: {str(e)}")
    return None, None

def update_product_links(markdown_text, user=None, uploaded_image_url=None):
    """
    마크다운 내 "[제품명](링크) - ..." 패턴을 찾아 처리합니다.
    """
    # TYPE으로 시작하는 텍스트를 h3로 변환
    pattern_type = re.compile(r'\*\*(TYPE [^*]+)\*\*')
    markdown_text = pattern_type.sub(r'### \1', markdown_text)

    # 기존의 제품 링크 처리
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)\s*-\s*(.*?)(?=\n|$)')

    def repl(match):
        product_name = match.group(1).strip()
        original_link = match.group(2).strip()
        description = match.group(3).strip() if match.group(3) else ""
        
        # "(현재 업로드하신 옷)" 처리
        if "(현재 업로드하신 옷)" in product_name:
            if uploaded_image_url:
                image_html = f'<div class="img-container"><img src="{uploaded_image_url}" alt="업로드한 옷"></div>'
                return f'<div class="item-container">상의: {image_html}</div>'
            return '<div class="item-container">상의: (업로드한 옷)</div>'
        
        # 다른 제품들 처리
        query = "무신사 스탠다드 " + product_name
        new_link, new_img = get_first_custom_search_image_info(query)
        
        if not new_link or not new_img:
            new_link = original_link
            new_img = ""
        
        # 이미지와 설명을 포함한 아이템 컨테이너 생성
        image_html = f'<a href="{new_link}" target="_blank" rel="noopener noreferrer"><div class="img-container"><img src="{new_img}" alt="{product_name}"></div></a>' if new_img else ""
        
        html_snippet = f'''
        <div class="item-container">
            <div class="item-title">
                <a href="{new_link}" target="_blank" rel="noopener noreferrer">{product_name}</a>
            </div>
            {image_html}
            <div class="item-description">{description}</div>
        </div>
        '''
        return html_snippet.strip()

    # 마크다운 변환
    updated = re.sub(pattern, repl, markdown_text)
    return updated

def convert_markdown_to_html(markdown_text):
    """
    markdown2 라이브러리로 마크다운 텍스트를 HTML로 변환합니다.
    """
    # 기본 변환만 수행하고 추가적인 pre 태그 래핑 없이 반환
    return markdown2.markdown(markdown_text)

# if __name__ == "__main__":
#     # 테스트할 마크다운 텍스트 예시
#     input_text = """
# ## 무신사 스탠다드 제품으로 완성하는 힙한 겨울 코디 😎

# **선택한 후드티:** 앞쪽에 영화 '엑소시스트' 포스터 프린팅이 있는 블랙 오버핏 후드티

# **날씨 & 체형 고려**: 🥶 현재 영하의 날씨이므로, 따뜻함을 유지하면서 170cm / 55kg 체형에 잘 어울리는 코디를 추천드립니다.

# ---

# **코디 1: 꾸안꾸 스트릿룩 🖤**

# * **상의**: 선택하신 '엑소시스트' 프린팅 블랙 후드티 👍
# * **하의**: [릴렉스드 스트레이트 히든 밴딩 크롭 데님 팬츠](https://www.musinsa.com/app/goods/3101574) - 루즈한 후드티와 밸런스를 맞춰줄 크롭 기장 데님 팬츠! 히든 밴딩으로 편안함까지 챙겼어요.
# * **신발**: [뮬 스니커즈](https://www.musinsa.com/app/goods/2102102) - 블랙 & 화이트 조합으로 깔끔함을 더하고, 겨울철 양말과 매치하기 좋은 스니커즈!
# * **액세서리**: [와이드 울 머플러](https://www.musinsa.com/app/goods/2765917) - 블랙 또는 네이비 컬러 머플러로 보온성과 스타일 지수를 동시에 UP!

# **코디 팁**: 오버핏 후드티와 크롭진의 조합은 트렌디하면서도 다리가 길어 보이는 효과를 줍니다. 

# ---

# **코디 2: 레트로 & 캐주얼 무드 🤎**

# * **상의**: 선택하신 '엑소시스트' 프린팅 블랙 후드티 👍
# * **하의**: [베이식 코듀ロイ 와이드 팬츠](https://www.musinsa.com/app/goods/3120698) - 레트로 감성을 더하는 코듀로이 소재의 와이드 팬츠! 블랙, 브라운 계열 추천!
# * **신발**: [레더 척테일러 1970S 하이](https://www.musinsa.com/app/goods/3146515) - 어떤 코디에도 잘 어울리는 컨버스 하이! 레더 소재로 겨울에도 따뜻하게 착용 가능합니다.
# * **액세서리**: [볼캡](https://www.musinsa.com/app/goods/2765883) - 심플한 디자인의 블랙 볼캡으로 힙한 무드를 더해보세요!

# **코디 팁**:  코듀로이 팬츠와 컨버스 하이 조합은 레트로한 무드를 극대화합니다. 프린팅 후드티와 함께 코디하여 유니크한 매력을 뽐내보세요. 
#     """

#     input_text="""# 테스트
# ## 🥶  쌀쌀한 겨울 날씨, 엑소시스트 후드티로 완성하는 스타일리시한 코디!

# **🎬 강렬한 엑소시스트 후드티를 메인으로, 따뜻하면서도 힙한 무드를 더해줄 무신사 스탠다드 아이템들을 추천할게요!**

# **TYPE 1: 캐주얼 스트릿룩 🔥**

# - 상의: (현재 업로드하신 옷)
# - 하의: [무신사 스탠다드 베이식 릴렉스 스웨트팬츠 블랙](https://www.musinsa.com/app/goods/2444794/0) - 후드티와 같은 블랙 컬러 스웨트팬츠로 통일감을 주면서 편안한 무드를 연출! 릴렉스 핏으로 활동성도 높여줍니다.
# - 신발: [무신사 스탠다드 레더 믹스 스니커즈 블랙](https://www.musinsa.com/app/goods/3153516/0) - 시크한 블랙 스니커즈는 어떤 코디에도 잘 어울리는 데일리템! 스웨트팬츠와 함께 스트릿한 무드를 완성해줍니다.

# **TYPE 2: 믹스매치 시크룩 😎**

# - 상의: (현재 업로드하신 옷) 
# - 하의: [무신사 스탠다드 울 블렌드 플레어 팬츠 차콜](https://www.musinsa.com/app/goods/3180553/0) - 캐주얼한 후드티에 세련된 플레어 팬츠를 매치하여 믹스매치룩 완성! 차콜 컬러는 시크한 분위기를 더해줍니다.
# - 신발: [무신사 스탠다드 첼시 부츠 블랙](https://www.musinsa.com/app/goods/3624799/0) - 첼시 부츠는 시크함과 따뜻함을 동시에 잡아주는 겨울철 필수템! 플레어 팬츠와 함께 다리가 길어 보이는 효과까지!

# **👍 어떤 코디를 선택하시든, 따뜻한 아우터는 필수!**

# - [무신사 스탠다드 푸퍼 숏패딩 블랙](https://www.musinsa.com/app/goods/2766990/0) - 어떤 코디에도 잘 어울리는 깔끔한 디자인의 숏패딩은 보온성까지 놓치지 않았습니다. 
# """
#     updated_markdown = update_product_links(input_text)
#     body_html = convert_markdown_to_html(updated_markdown)
#     full_html = f"""<!DOCTYPE html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>무신사 스탠다드 제품 기반 코디 추천</title>
# </head>
# <body>
# {body_html}
# </body>
# </html>"""
#     print(full_html)
