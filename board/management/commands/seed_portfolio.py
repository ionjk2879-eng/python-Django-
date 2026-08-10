from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Profile
from board.models import Comment, Post, PostImage


class Command(BaseCommand):
    help = 'Coffee Log 포트폴리오 화면과 동일한 데모 콘텐츠를 생성합니다.'

    def handle(self, *args, **options):
        demo_dir = Path(settings.BASE_DIR) / 'board/static/img/demo'
        user_specs = {
            'barista_log': ('민준', 'barista@coffeelog.demo', '좋은 원두와 오래 쓰는 도구를 기록합니다.', '서울', 'avatar-barista-log.png'),
            'bean_hunter': ('서연', 'beans@coffeelog.demo', '새로운 산지와 향미를 찾아다니는 원두 탐험가입니다.', '부산', 'avatar-bean-hunter.png'),
            'slow_pour': ('지우', 'recipe@coffeelog.demo', '한 잔의 변수를 천천히 기록하는 홈브루어입니다.', '대전', 'avatar-slow-pour.png'),
            'homecafe_day': ('하린', 'homecafe@coffeelog.demo', '매일의 라테와 계절 음료를 소개합니다.', '인천', 'avatar-homecafe-day.png'),
        }
        users = {}
        for username, (name, email, bio, location, avatar_name) in user_specs.items():
            user, _ = User.objects.get_or_create(username=username)
            user.first_name, user.email = name, email
            user.set_password('CoffeeLog2026!')
            user.save()
            users[username] = user
            profile, _ = Profile.objects.get_or_create(user=user)
            stored_avatar = f'profiles/{avatar_name}'
            source = demo_dir / avatar_name
            if source.exists() and not default_storage.exists(stored_avatar):
                default_storage.save(stored_avatar, ContentFile(source.read_bytes()))
            profile.bio, profile.location = bio, location
            if default_storage.exists(stored_avatar):
                profile.avatar.name = stored_avatar
            profile.save()

        Post.objects.filter(author__in=users.values()).delete()
        posts_data = [
            {
                'title': '에티오피아 구지 내추럴, 복숭아 향을 살린 레시피', 'author': 'slow_pour',
                'category': Post.Category.RECIPE, 'views': 1248, 'image': 'post-guji-recipe.png',
                'tags': '에티오피아, 구지, 내추럴, V60',
                'bean_amount': '20g', 'water_amount': '300g', 'water_temperature': '92℃',
                'brew_time': '2분 40초 ~ 3분 10초', 'brew_tool': '하리오 V60 02 · 코만단테 24클릭',
                'content': '에티오피아 구지의 내추럴 커피는 잘 익은 복숭아, 자두, 베리류의 달콤한 향미가 매력적입니다.\n이번 레시피는 과일의 향을 선명하게 살리면서, 클린하고 부드러운 단맛의 균형을 잡는 데 초점을 두었습니다.\n\n1. 0:00 ~ 0:30　뜸들이기 — 40g의 물을 원을 그리며 부어 전체적으로 적셔줍니다.\n2. 0:30 ~ 1:10　1차 추출 — 중심에서 바깥으로 원을 그리며 100g까지 채웁니다.\n3. 1:10 ~ 1:50　2차 추출 — 180g까지 부어 수위를 유지하며 추출합니다.\n4. 1:50 ~ 2:30　3차 추출 — 300g까지 부어 균일하게 마무리합니다.\n5. 2:40 이후　드리퍼를 제거하고 가볍게 스월링 후 서빙합니다.\n\nTIP　내추럴 커피는 추출 온도를 90~93℃ 사이로 유지하면 과일 향이 더 선명하게 표현됩니다.'
            },
            {'title': '콜롬비아 핑크 버번 첫 시음 노트', 'author': 'bean_hunter', 'category': Post.Category.TASTING, 'views': 986, 'image': 'post-pink-bourbon.png', 'tags': '콜롬비아, 핑크버번, 시음', 'content': '핑크 버번 원두의 과일 향과 산미가 정말 인상적이었습니다. 오렌지 블로섬과 홍차, 살구와 꿀 같은 단맛이 온도에 따라 차례로 느껴집니다. 첫 시음 노트를 공유합니다.'},
            {'title': '케냐 키암부 워시드 — 블랙커런트와 토마토 사이', 'author': 'bean_hunter', 'category': Post.Category.TASTING, 'views': 812, 'image': 'post-kenya-cherries.png', 'tags': '케냐, 키암부, 워시드', 'content': '산미가 살아있으면서도 클린한 케냐 워시드의 매력을 다시 느꼈습니다. 뜨거울 때는 블랙커런트, 식으면서 자두와 토마토를 닮은 감칠맛이 이어집니다.'},
            {'title': '입문용 핸드밀 3종, 한 달 사용 후 솔직 비교', 'author': 'barista_log', 'category': Post.Category.GEAR, 'views': 1532, 'image': 'post-hand-grinders.png', 'tags': '핸드밀, 장비, 입문', 'content': '분쇄 균일도, 다이얼 조절, 그립감과 청소 편의성을 기준으로 입문용 핸드밀 세 가지를 한 달 동안 비교했습니다. 매일 쓰는 도구인 만큼 숫자보다 손에 잡히는 감각이 중요했습니다.'},
            {'title': '에스프레소용 원두 분쇄도, 어떻게 조절하시나요?', 'author': 'barista_log', 'category': Post.Category.GEAR, 'views': 734, 'image': 'post-espresso-grind.png', 'tags': '에스프레소, 분쇄도, 장비', 'content': '최근 추출이 자꾸 불안정해져 분쇄도 조절 기준을 다시 정리했습니다. 도징량과 수율을 고정하고 추출 시간에 따라 한 단계씩 조절하는 방법을 공유합니다.'},
            {'title': '고소한 원두 추천 부탁드려요!', 'author': 'homecafe_day', 'category': Post.Category.BEANS, 'views': 643, 'image': 'post-nutty-pourover.png', 'tags': '고소한 원두, 추천, 홈카페', 'content': '우유와 잘 어울리는 고소한 원두를 찾고 있어요. 견과류와 초콜릿의 단맛이 선명하고 산미가 편안한 원두가 있다면 추천 부탁드립니다.'},
            {'title': '싱글오리진 원두 보관법, 여러분은 어떻게 하시나요?', 'author': 'homecafe_day', 'category': Post.Category.BEANS, 'views': 611, 'image': 'post-bean-storage.png', 'tags': '싱글오리진, 원두 보관, 신선도', 'content': '향과 신선도를 오래 유지하기 위한 보관 팁이 궁금합니다. 소분 냉동과 밸브백 실온 보관을 비교한 경험을 나눠주세요.'},
        ]
        posts_data.append({
            'title': '브라질 세하도 내추럴, 데일리 커피로 마셔본 후기',
            'author': 'bean_hunter',
            'category': Post.Category.BEANS,
            'views': 928,
            'image': 'post-brazil-cerrado.png',
            'tags': '브라질, 세하도, 내추럴, 데일리커피',
            'content': (
                '브라질 세하도 지역의 내추럴 원두를 일주일 동안 에스프레소와 핸드드립으로 마셔봤습니다.\n\n'
                '구운 아몬드와 밀크초콜릿을 닮은 고소한 향이 중심을 잡고, 식으면서 은은한 건과일 단맛이 이어집니다. '
                '산미가 강하지 않아 매일 편안하게 마시기 좋았고 우유를 더했을 때도 커피의 맛이 선명했습니다.\n\n'
                '핸드드립은 원두 20g, 물 300g, 91℃에서 2분 50초 전후로 추출했을 때 가장 균형이 좋았습니다. '
                '고소하고 단 커피를 좋아하거나 홈카페용 데일리 원두를 찾는 분께 추천합니다.'
            ),
        })
        now, posts = timezone.now(), []
        for index, data in enumerate(posts_data):
            image_name = data.pop('image')
            author_name = data.pop('author')
            views = data.pop('views')
            post = Post.objects.create(author=users[author_name], view_count=views, **data)
            Post.objects.filter(pk=post.pk).update(created_at=now - timedelta(hours=index * 3 + 1))
            storage_name = f'posts/demo/{image_name}'
            source = demo_dir / image_name
            if source.exists() and not default_storage.exists(storage_name):
                default_storage.save(storage_name, ContentFile(source.read_bytes()))
            if default_storage.exists(storage_name):
                PostImage.objects.create(post=post, image=storage_name, alt_text=f'{post.title} 대표 이미지')
            posts.append(post)

        comments = [
            ('bean_hunter', '복숭아 향 정말 좋아하는데 레시피 감사합니다! 혹시 물은 어떤 제품을 사용하셨나요?'),
            ('slow_pour', '저는 연수(경도 50mg/L 내외) 사용했어요. 산미가 더 또렷하게 올라왔습니다.'),
            ('homecafe_day', '1:10부터 1:50까지 물줄기 굵기는 어느 정도가 좋을까요?'),
        ]
        for username, text in comments:
            Comment.objects.create(post=posts[0], author=users[username], content=text)

        posts[0].bookmarked_by.add(users['barista_log'], users['bean_hunter'])
        posts[0].liked_by.add(*users.values())
        for post in posts[1:5]:
            post.bookmarked_by.add(users['barista_log'])
            post.liked_by.add(users['homecafe_day'], users['slow_pour'])
        self.stdout.write(self.style.SUCCESS('스크린샷용 사용자 4명, 이미지 게시글 7개, 레시피와 저장 데이터를 생성했습니다.'))
