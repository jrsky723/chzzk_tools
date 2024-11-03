import datetime

# 주어진 데이터 문자열
data = """
POLO
영비 (Young B)
2:39:46 - 2:41:15
Ring My Bell (Feat. 나얼 Of Brown Eyed Soul)
Dynamicduo
5:32 - 6:52
Selfmade Orange 2 (feat. Changmo, Paul Blanco)
SUPERBEE
3:47:17 - 3:48:03
Slow Heartbeat (feat. Ja Mezz)
Layone
2:17:01 - 2:17:41
Sujak
XXX
6:22:33 - 6:25:02
About Muse
Don Malik, Mild Beats
4:47:57 - 4:49:25
Airbag ft. 나얼
TABLO
1:02:28 - 1:03:50
BOUNTY HUNTER (feat. COKE JAZZ)
B-Free
5:22:58 - 5:24:13
Sushi (JM Remix)
Goretexx, GIRIBOY, Black Nut, BILL STAX, Swings
6:15:56 - 6:16:47
Boogie On & On
Beenzino
5:09:15 - 5:10:23
Traffic Control(교통정리) (Feat. Heize(헤이즈))
GIRIBOY(기리보이)
6:07:35 - 6:08:28
우리가 빠지면 Party가 아니지 Ain’t No Party Like an AOMG Party (Clean Version)
박재범 Jay Park & Ugly Duck
1:36:32 - 1:37:50
지구 멸망 한 시간 전
Jclef
8:44 - 10:11
Chool Check (Feat. Naul For Brown Eyed Soul)
Dynamicduo
28:26 - 29:54
땡땡땡 Dang Dang Dang
Supreme Team
3:23:50 - 3:25:28
지붕 위의 바이올린
Primary Skool
4:46:24 - 4:47:27
My Team (feat. REDDY, Okasian, Huckleberry P, Paloalto & Keith Ape)
B-Free
52:32 - 53:45
우산 (Feat. 윤하)
에픽하이
2:10:31 - 2:10:57
ceci n'est pas une pipe
Khundi Panda
2:09:44 - 2:10:19
Earth(지구) (Prod. By dnss) (Feat. Benzamin)
NO:EL
4:51:20 - 4:53:11
마이동풍
배치기
1:12:02 - 1:13:21
Stupid in love
Soyou, Mad Clown
2:11:24 - 2:12:02
Speed Racer (feat. All Memberz)
Outsider
2:41:20 - 2:41:53
1219 Epiphany
버벌진트 (Verbal Jint)
32:42 - 34:59
Just Like This (Feat. george)
Loco
3:45:17 - 3:45:43
Bokdukbang
Northfacegawd
1:16:40 - 1:17:33
MOMM (Feat. JUSTHIS) (Prod. 코드 쿤스트 CODE KUNST)
Kid Milli
2:47:37 - 2:48:08
iffy (Prod. GroovyRoom)
Sik-K, pH-1, Jay Park, GroovyRoom
3:00:38 - 3:01:41
Officially Missing You
긱스 (Geeks)
5:04:33 - 5:06:06
독기
아이언
4:00:18 - 4:01:36
Swoosh Flow Remix (Feat. 365lit, ZENE THE ZILLA, Chamane, Paul Blanco, Damndef, Keem Hyo-Eun & Northfacegawd)
CHANGMO
3:16:19 - 3:17:20
NoNo (Feat. 사이먼 도미닉 Simon Dominic) (Prod. 코드 쿤스트 CODE KUNST)
루피 (Loopy)
6:06:17 - 6:07:21
Pass the Rhyme (feat. Changmo, Dok2)
SUPERBEE(슈퍼비)
50:27 - 52:00
Because Of You (Feat. Soulman)
Supreme Team
25:38 - 27:00
KOCEAN
Kid Milli
3:13:37 - 3:14:05
어깨
양동근
1:51:03 - 1:51:57
Hogu(호구) (Prod.by Fisherman of wybh) (feat.BrotherSu(브라더수))
GIRIBOY(기리보이)
4:38:05 - 4:39:34
멀어 Too Far (Feat. Beenzino)
프라이머리 Primary
4:11:48 - 4:13:54
flex (Prod. By GIRIBOY(기리보이))
GIRIBOY(기리보이), Kid Milli, NO:EL, Swings(스윙스)
4:05:49 - 4:06:51
마법의 성
MC Sniper
5:00:15 - 5:02:04
The Purge
Jay Park, pH-1, BIG Naughty, Woodie Gochild, HAON, TRADE L, Sik-K
27:05 - 28:07
Rap Badr Hari
허클베리피 (Huckleberry P)
3:52:08 - 3:52:55
One Of A Kind
G-DRAGON
1:27:42 - 1:28:54
Lights On
Geeks
3:29:17 - 3:30:52
BAAAM (Feat. Muzie of UV)
다이나믹 듀오 Dynamic Duo
3:20:44 - 3:21:35
Summer (Feat. BE’O)
Paul Blanco
5:27:15 - 5:28:40
VVS (Feat. JUSTHIS) (Prod. GroovyRoom)
Miranni , Munchman , Khundi Panda , MUSHVENOM
1:32:56 - 1:33:34
Click Me (Feat. Dok2)
Zion.T
1:57:20 - 1:58:39
I Could Do Dead
디보 (Dbo)
4:18:31 - 4:19:59
Story Of someone I know (inst)
San E
3:50:29 - 3:51:45
Lights out
TakeOne
4:25:31 - 4:27:07
POWER
Fana
37:35 - 38:48
내가(Feat. Beenzino & The Quiett)
Dok2 (도끼)
2:58:09 - 2:58:57
ITX (Feat. CHANGMO)
ZENE THE ZILLA
59:02 - 1:00:18
Tomorrow (Feat. GIRIBOY, BIG Naughty)
lIlBOI
3:10:38 - 3:11:39
I Laugh Now(원래 난 이랬나)
C JAMM
3:21 - 3:43
나만 모르게 Unknowingly (Feat. T)
Supreme Team
3:52:59 - 3:54:23
즐거운 생활
45RPM
1:35:26 - 1:36:09
Then Then Then
Supreme Team, Young Jun
24:05 - 25:30
Frank Ocean (feat. Javan)
Jiho Givenchy
1:22:19 - 1:23:21
불한당가
NUCK
3:31:44 - 3:33:23
Prime Time Remix (With ODEE, CHANGMO, Hash Swan & Dok2)
The Quiett
3:14:48 - 3:15:59
MOSS (Feat. MINO & BOBBY) (Prod. by MINO)
Mudd the student
3:46:20 - 3:47:13
우리가 얼마나 WURIGA (Feat. EK, Bola, Neal) (Prod. by Neal)
MBA(Most Badass Asian)
3:08:11 - 3:09:17
배인(VAIN)(Feat. Koonta of Rude Paper)
언터쳐블 Untouchable
4:37:51 - 4:39:30
Yooooo (Feat. Kid Milli, sokodomo, Polodared)
Lil Moshpit
3:28:04 - 3:29:07
BAND
창모 CHANGMO, Hash Swan, ASH ISLAND, 김효은 Keem Hyo-Eun
3:17:25 - 3:18:07
한강 gang han gang gang (Feat. Byung Un & CHANGMO)
The Quiett
2:22:14 - 2:23:39
High High [Live]
BIGBANG
5:36:16 - 5:37:26
Rain Showers Remix
Just Music
5:41:02 - 5:41:55
Beer(비워) (Prod.Way Ched)
CHANGMO, Hash Swan, ASH ISLAND, KEEM HYOEUN(김효은), Leellamarz & The Quiett
5:19:46 - 5:20:37
Organ
코드 쿤스트 (Code Kunst)
4:29:24 - 4:30:32
UGK (Feat. Paloalto)
Hwaji
1:21 - 2:59
Text Me
DPR LIVE
45:12 - 46:35
Memoirs
Gwangil Jo
3:06:25 - 3:07:29
시차 (We Are) (Feat. 로꼬 & GRAY)
우원재
6:18:03 - 6:19:14
SSKK
C JAMM
2:35:58 - 2:37:21
Park Sang Hyuk
Huckleberry P
4:57:19 - 4:58:37
빌었어 wish
창모 CHANGMO
1:52:16 - 1:53:25
400km (Feat. Kid Milli)
Han Yo Han
4:24:57 - 4:25:25
Laputa (feat. Crush)
DPR LIVE
48:51 - 50:22
Always Awake
Jazzyfact
3:54:54 - 3:55:55
ROSE (Feat. Skinny Brown, Homeboy)
Young B(영비)
20:10 - 21:56
I'mma Overcome
Swings
39:35 - 41:41
불꽃놀이 (Fireworks)
Dynamic Duo
6:34:40 - 6:35:28
One (Feat. 지선)
에픽하이
4:13:20 - 4:14:04
YGGR (Feat. MC Meta)
ILLIONAIRE RECORDS
2:29:57 - 2:30:38
Hey
C JAMM, YANGHONGWON
6:13:39 - 6:14:52
Goldie
A$AP Rocky
4:41:54 - 4:42:07
Flowdown (Feat. 화나 ＆ 탁 Of 배치기)
Mad Clown
3:41:34 - 3:42:29
달이 뜨면 (광대)
정상수
2:50:03 - 2:52:12
Go Back (Feat. Jung In)
Dynamicduo
1:20:41 - 1:21:50
아까워
Jazzyfact
2:37:25 - 2:38:44
좋아 Joah
박재범 Jay Park
43:11 - 44:28
Where U At? (Simon D Solo)
Supreme Team
5:54:10 - 5:56:03
Youth
Owen
1:31:02 - 1:32:22
투올더힙합키즈 투
Verbal Jint
2:14:02 - 2:15:17
맵고짜고단거 (Feat. 페노메코)
다이나믹 듀오 Dynamicduo
4:54:49 - 4:56:09
Do Not Go Gentle Into That Good Night (Feat. KWAII, DON MALIK, GongGongGoo009) (Prod. Humbert)
JUSTHIS
4:07:18 - 4:08:29
Oscar
pH-1, Golden, BIG Naughty, Jay Park
1:23:25 - 1:24:41
Smoking Dreams
Jazzyfact
4:49:40 - 4:51:10
How Do I Look?
빈지노 (Beenzino)
3:34:34 - 3:36:15
Lost Chronicle
IGNITO
2:00:46 - 2:01:31
Dali, Van, Picasso
빈지노 Beenzino
1:55:16 - 1:56:41
Tech Fleece Freestyle (feat. KHAN & hangzoo)
NSW yoon
2:43:50 - 2:45:02
Spread the Word Remix (feat. G2, Play$tar & Qim Isle) (Spread the Word Remix Version)
Okasian, REDDY, Keith Ape
3:03:18 - 3:04:39
야망 AMBITION (Feat. ASH ISLAND, 김효은 KEEM HYO-EUN, Hash Swan, CHANGMO) (Prod. TOIL)
Leellamarz
5:31:40 - 5:32:30
Pokerface(포커페이스)
C JAMM
5:34:39 - 5:35:48
DAx4
사이먼 도미닉 Simon Dominic
2:28:10 - 2:29:55
Red Sun (Feat. ZICO, Swings)
Hangzoo
5:28:40 - 5:30:12
말어 (With Okasian)
Hwaji, Okasian
4:31:35 - 4:32:26
Chik Chik Pok Pok Freestyle (Feat. Jvcki Wai & SIMO of Y2K92)
Woo
5:14:28 - 5:14:45
화장 지웠어 (No Make Up) (Feat. Zion- T, HA:TFELT)
개코 Gaeko
12:13 - 13:30
YOUTH!
BOYCOLD
2:15:52 - 2:16:43
No One (feat.Sunwoo Jung-A)
JUSTHIS
1:58:58 - 2:00:31
Abu Dhabi (With. Skinny Brown, Leellamarz, Sik-K)
The Quiett
10:39 - 12:00
너희가 힙합을 아느냐?
Drunken Tiger
2:18:22 - 2:19:47
Heartless
퓨처리스틱 스웨버 (Futuristic Swaver)
1:13:34 - 1:14:31
Skyscraper (Feat. JUSTHIS)
DON MALIK
4:32:34 - 4:33:29
Cooler Than the Cool (feat. Huckleberry P)
JUSTHIS, Paloalto
5:48:29 - 5:49:54
전혀 Not at all (Feat. 우원재 Woo Won Jae) (Prod. GroovyRoom)
Various Artists
5:36:33 - 5:37:09
Jasmine
DPR LIVE
46:53 - 48:27
NFS
Nucksal
57:40 - 58:50
DONGHAE
Jayho
6:34:57 - 6:36:14
죽일 놈 (Guilty)
Dynamic Duo
1:08:24 - 1:10:02
Tiger Den (Feat. Jvcki Wai)
GIRIBOY
1:43:26 - 1:44:27
changes (feat. Loopy)
Owen
6:26:50 - 6:28:00
Get Fresh
리짓군즈 Legit Goons
5:18:28 - 5:19:41
거북선 (Feat. 팔로알토)
자메즈, 앤덥, 송민호
4:13:55 - 4:14:25
All By Myself
Defconn
1:10:50 - 1:11:44
Damn! (Feat. Black Nut(블랙넛))
NO:EL
2:05:22 - 2:06:13
작업
오왼 오바도즈 (Owen Ovadoz)
1:24:53 - 1:25:55
곡예사
조광일
5:11:46 - 5:12:43
khalifa
unofficialboyy, Jazzy Moon
5:15:04 - 5:15:59
zoom
염따 YUMDDA
3:19:39 - 3:20:40
안산 느와르 (feat. RingoJay)
Chaboom
5:24:15 - 5:25:43
Motherfucker Pt. 2
JUSTHIS
2:01:52 - 2:03:47
Jail
nafla
1:29:02 - 1:30:17
Drought (feat. Beenzino)
Paloalto
5:59:25 - 6:00:24
봄이여 오라 Feat. 유리
MC Sniper
6:02:06 - 6:04:02
Neo Christian Flow
BewhY, Simba Zawadi
3:18:26 - 3:19:37
Born Hater ft. Beenzino, Verbal Jint, B.I, Mino, Bobby
EPIK HIGH
14:09 - 15:44
It's All Good (feat.Tyra)
Swings
3:59:00 - 4:00:13
Now(지금) (Feat. Okasian)
Uneducated Kid
2:46:31 - 2:47:27
4 Seasons(1.12)
YANGHONGWON
6:00:36 - 6:01:59
Business class (Feat. JUSTHIS)
Young B(영비)
4:42:33 - 4:43:47
외톨이
아웃사이더 
4:20:48 - 4:21:46
Battlecry (Bonus Track)
Mad Clown
4:03:17 - 4:03:34
Shit Is Real (Feat. The Quiett, GIRIBOY(기리보이), Kid Milli) (Prod. By IOAH)
Swings(스윙스)
3:37:35 - 3:38:28
GOTT (Feat. MOON, 우원재 Woo & Jvcki Wai)
사이먼 도미닉 Simon Dominic
4:27:49 - 4:28:40
Simon Dominic
Simon Dominic
5:40:13 - 5:41:01
빈차(Home Is Far Away) ft. OH HYUK M/V
EPIK HIGH
1:02:28 - 1:03:11
New Kings (Feat. JUSTHIS, Young B & The Quiett)
김효은 KEEM HYO EUN
5:56:07 - 5:57:23
Bulldozer
Swings
16:36 - 17:54
무투
Garion
2:55:04 - 2:56:09
Malibu (Feat. The Quiett, Mokyo) (Prod. Mokyo)
pH-1
2:45:08 - 2:46:07
Gloomy Sunday
MC Sniper
1:38:36 - 1:39:40
alchemy (Feat. Dok2, MINO)
Ja Mezz
1:50:08 - 1:50:31
F the World - Remaster
Mommy Son
6:11:48 - 6:13:03
Germination
Fana
5:45:17 - 5:46:41
It Takes Time (Feat. Colde)
Loco
22:26 - 24:02
John Cena (feat. Northfacegawd, JUSTHIS, Layone)
Yumdda
4:20:10 - 4:20:26
될 대로 되라고 해 Feel so good (느낌 So Good)
개코 Gaeko
5:50:56 - 5:52:02
Tomorrow ft. TaeYang
TABLO
1:34:22 - 1:35:26
Junk Flavor
Lil tachi, Young B, YUNHWAY, JUSTHIS
1:45:35 - 1:46:30
Hold Me Tight (Feat. Crush)
Loco
2:48:48 - 2:49:59
하기나 해(Feat. Loco)
GRAY
4:09:21 - 4:10:16
History Is Made at Night (feat. Simon Dominic)
Huckleberry P
1:46:52 - 1:47:40
Puzzle
오왼 오바도즈 (Owen Ovadoz)
5:25:46 - 5:27:13
You Don′t Know
Loco
4:15:52 - 4:17:00
Selfmade Orange (Feat. SUPERBEE)
창모 (CHANGMO)
7:30 - 8:38
입장정리 Friendzone (Feat. 최자 CHOIZA, Simon D)
프라이머리 Primary
35:37 - 37:12
Anything (feat. Kimparkchella)
B-Free
5:52:03 - 5:54:06
겁 (Feat. 태양)
송민호
2:03:52 - 2:04:30
IMJMWDP (Prod. By GIRIBOY)
GIRIBOY, NO:EL, Black Nut, Young B, Osshun Gum, YUNHWAY, JUSTHIS, Jvcki Wai, Kid Milli, Han Yo Han
4:44:00 - 4:44:41
전화번호(Phone Number)
JINUSEAN
2:12:56 - 2:13:54
울타리 a fence
우원재 Woo
6:10:14 - 6:11:40
run! (feat. JUSTHIS)
nafla
3:04:42 - 3:05:48
DEADMAN (Feat. Changmo, Chaboom) (Prod. Conda)
BLNK
5:21:30 - 5:22:46
나쁜 피 (Bad Blood) Bad Blood
매드 클라운 (Mad Clown)
55:59 - 57:04
Playaplayaplaya
Samuel Seo
41:59 - 43:08
You look Good (좋아보여)
Verbal Jint
3:49:13 - 3:50:00
Cheap talk (Feat. JUSTHIS) (Prod. CODE KUNST)
Gaeko
3:56:14 - 3:56:53
작두 (Feat. 넉살, Huckleberry P) Cut Cut Cut (Nucksal, Huckleberry P)
딥플로우 Deepflow
5:57:36 - 5:58:31
Trip (Feat. Hannah)
Leellamarz
6:30:37 - 6:31:27
Hot Summer
B-Free
3:54 - 5:25
No One Likes Us (Prod. Nochang)
Swings, Nochang, Black Nut, DAMINI
3:33:28 - 3:33:56
I turned off the TV... (feat. Yoon Mirae & 10cm)
Leessang
5:02:05 - 5:03:46
Martini Blue
DPR LIVE
6:21:05 - 6:22:33
Bumper Car(범퍼카) (Feat. NO:EL, Young B)
HAN YO HAN(한요한)
3:58:26 - 3:58:53
The Difference in Caliber(그릇의 차이)
Swings(스윙스)
2:53:26 - 2:54:23
광대 | Clowns (with B.M.K)
리쌍 (LeeSSang)
5:43:42 - 5:44:33
Y
프리스타일
6:02:58 - 6:04:06
PICK IT UP (feat. A$AP Rocky)
Famous Dex
4:34:15 - 4:34:30
The Anecdote
E SENS
5:06:08 - 5:07:30
Diamonds
Owen
5:33:22 - 5:34:39
남자기 때문에
Drunken Tiger
5:16:45 - 5:18:18
Everest
허클베리피 (Huckleberry P)
2:19:51 - 2:21:20
Beautiful (Feat. Skinny Brown)
ASH ISLAND
1:54:03 - 1:55:00
Romantic winter (feat.Kim Jin Ho of SG Wannabe)
Kim Jinpyo
4:43:22 - 4:44:20
귀감 gui gam (Feat. ZENE THE ZILLA)
The Quiett
1:26:12 - 1:27:24
호불호 Taste (Feat. 기리보이 GIRIBOY) (Prod. By GRAY)
우원재 (Woo)
1:42:04 - 1:43:16
인생 (Feat. 웅산)
MC Sniper
2:23:54 - 2:26:22
바코드 Bar Code (Prod. GroovyRoom)
김하온 HAON, 이병재 Vinxen
4:53:40 - 4:54:49
알렉산더처럼 왕 Wang Like Alexander (Feat. GRAY)
Hash Swan
6:25:22 - 6:26:39
Heu ! (Full Ver.)
수퍼비 SUPERBEE
2:06:52 - 2:07:14
Worldwide (Feat. Dok2 & The Quiett)
박재범 Jay Park
3:01:56 - 3:03:09
[MV] Carnival Gang(카니발갱)
Goretexx
2:32:50 - 2:33:48
Beenzino
Black Nut
5:45:08 - 5:46:40
GOTTASADAE
BewhY
3:11:42 - 3:12:45
All I Wanna Do (Feat. Hoody & 로꼬 Loco) (Korean Version)
박재범 Jay Park
4:35:19 - 4:36:23
D (Half Moon)
DEAN
4:10:17 - 4:11:40
100 (feat.Nochang)
Black Nut
3:44:11 - 3:45:07
주소
코드 쿤스트 (CODE KUNST)
4:23:50 - 4:24:50
KILLA DREADS
SKULL, C Jamm, Jah Vinci
30:07 - 31:49
Ooh La La
팔로알토 (Paloalto), 스월비 (Swervy), 허클베리피 (Huckleberry P), 스웨이디 (Sway D)
1:17:52 - 1:18:45
MELODY
ASH ISLAND
1:00:22 - 1:01:49
Downtown Baby
BLOO
18:47 - 20:05
ON IT + BO$$
릴보이, 로꼬, 박재범
2:33:53 - 2:34:41
WONHYO
Layone
5:08:24 - 5:09:14
Ras-Hop No todo es tristeza
Ras-Hop
6:33:25 - 6:34:41
"""  # 생략된 부분이 있으면 추가

# 곡 정보를 저장할 리스트
songs = []

# 데이터 문자열을 줄 단위로 나누기
lines = data.strip().splitlines()

# 세 줄씩 순회하면서 곡 정보 추출
for i in range(0, len(lines), 3):
    title = lines[i].strip()  # 곡 제목
    artist = lines[i + 1].strip()  # 아티스트명
    time_range = lines[i + 2].strip()  # 시간 범위
    print(time_range)
    try:
        # 시작 시간만 추출
        start_time_str = time_range.split(" - ")[0].strip()
        # 시간 포맷에 따라 파싱
        if ":" in start_time_str:
            time_format = "%H:%M:%S" if start_time_str.count(":") == 2 else "%M:%S"
            start_time = datetime.datetime.strptime(start_time_str, time_format)
    except ValueError:
        print(f"시간 정보를 읽는 중 오류가 발생했습니다: {time_range}")
        continue

    # 곡 정보를 튜플로 추가
    songs.append((start_time, title, artist))

# 시작 시간으로 정렬
songs.sort(key=lambda x: x[0])

# 정렬된 곡 정보를 파일로 저장
with open("sorted_songs.txt", "w", encoding="utf-8") as file:
    for start_time, title, artist in songs:
        # 출력 형식에 맞게 시간 포맷팅
        formatted_time = (
            start_time.strftime("%H:%M:%S")
            if start_time.hour
            else start_time.strftime("%M:%S")
        )
        file.write(f"{formatted_time} {artist} - {title}\n")

print("sorted_songs.txt 파일에 저장이 완료되었습니다.")
