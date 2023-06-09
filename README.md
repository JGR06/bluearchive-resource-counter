# BlueArchive Resources Counter

블루아카이브의 각종 성장재화를 집계하기 위한 스크립트입니다. 

[Justin163's Resource Planner](https://justin163.com/planner/) 에 재화를 집계해 넣을 때 더 편하게 하기 위해 만들어졌습니다.

## Disclaimer

1. 이 스크립트는 [ImageMax](https://cafe.naver.com/imagemax/3) 라는 프로그램에 종속적입니다. 타깃 윈도우를 지정해 이미지인식을 통해 자동화를 도와주는 프로그램입니다.
   - 현재 이 스크립트가 작성된 버전의 ImageMax 무료버전 바이너리가 게재되어 있습니다.
   - 라이센스는 프로젝트 최상단에 명시되어 있습니다.
   - 또한 해당 프로그램에서 OCR인식을 영어, 한국어, 숫자만 지원하는 점에 따라 어차피 글로벌버전 유저는 사용할 수 없기때문에 리드미는 한글로 작성되었습니다.

2. 앱플레이어의 해상도가 1920\*1080(280dpi) 이외일 경우 이미지 인식이 원활히 되지 않을 수 있습니다.
   - 현재 1600\*900(240dpi) 해상도까지는 추가로 지원합니다.
   - 해상도와 dpi를 맞추지 않으면 정상작동을 보장할 수 없습니다. 또한 개개인의 설정에 따라 미세하게 차이가 나 인식하지 못하는 경우가 있습니다.
   - 따라서 처음 사용하실 때 어떤 이미지를 인식하지 못하는지 한 번은 확인하고 ROI를 수정하거나 유사도 허용치를 넓혀주는 작업을 해보시면 좋습니다.
   - 이외의 해상도에서는 애석하게도 아이템 이미지를 다시 캡쳐해야할 수 있습니다.


## Installation

### Dependency
- [Python 3.10+](https://www.python.org/downloads/)
  - 설치시 반드시 `Add Python 3.10 to PATH`에 체크해주셔야합니다.
  - 이미 파이썬이 설치돼있는 경우 PATH 등록이 잘 안되는 경우가 있습니다. 그럴 경우에는 환경 변수 관리자에 들어가서 직접 PATH에 등록된 파이썬 경로를 수정해주시면 원활히 작동합니다.
  - ![_readme_attachment_0_python_install](https://user-images.githubusercontent.com/2003010/230747469-1d36c610-2815-437e-8dfa-e20bdb41b2ef.png)
  - 설치 후 `Disable PATH length limit` 버튼이 출력된다면 클릭해서 PATH 길이 제한을 없애주세요.
  - ![_readme_attachment_1_python_install](https://user-images.githubusercontent.com/2003010/230747568-322472b3-785a-4ce9-90e4-093bfc312f24.png)
- [ImageMax v2.15](https://cafe.naver.com/imagemax/3)
  - 현재 저장소에 있으니 추가로 다운로드하실 필요는 없습니다. 사용법이나 주의사항 등이 궁금하시면 둘러보시면 됩니다.
- LDPlayer, Bluestacks 등의 앱플레이어
  - 해당 스크립트는 LDPlayer9 에서 테스트하며 개발됐습니다.
- [Justin163's Resource Planner](https://justin163.com/planner/)
  - 해당 스크립트는 위 사이트를 더 편리하게 이용하기 위해 만들어졌습니다.
  - 당장 다른 재화관리 사이트를 사용한 적이 없기때문에 현재 버전에서는 다른 사이트를 지원하지 않습니다.

이외에 별도의 설치는 필요 없습니다.

## Usage

### \*. 본인의 앱플레이어 해상도가 1920\*1080이 아니라면
`switch_resolution` 폴더에 들어가서 `switch.bat`을 더블클릭해 실행해주세요.

기본으로 1600\*900으로 전환되도록 설정되어있습니다.

현재 1920\*1080, 1600\*900 해상도만 지원되고 있습니다.

해상도를 추가하고 싶으시면 [아래 설명](#contribution)을 참고해주시면 됩니다.

### 0. 재화관리 사이트에서 본인의 데이터 가져오기(권장)
**해당 사이트를 사용한 적이 없다면 건너뛰어도 상관없지만, 본인의 데이터가 있다면 반드시 진행해주세요.**

[Justin163's Resource Planner](https://justin163.com/planner/)에 접속해서 하단의 `Transfer` 버튼을 누릅니다.

![_readme_attachment_2_planner_export](https://user-images.githubusercontent.com/2003010/230747761-cdffc04d-b8d6-4650-8f01-6cd6ac5894bf.png)

`Export`버튼을 누른 후 나오는 데이터를 복사해 `resource_counter/planner_exported.json`에 붙여넣어줍니다.

기본적으로 샘플 데이터가 들어가있습니다. `Ctrl + A`를 눌러 모두 선택해 지운 뒤 본인의 데이터를 덮어씌우시면 됩니다.

해당 데이터는 사용자의 백업용으로도 사용할 수 있습니다.

### 1. 앱플레이어와 `ImageMax.exe` 실행

**`ImageMax.exe` 실행시 `우클릭>관리자 권한으로 실행` 을 통해 실행해주세요.**

앱플레이어에서 블루아카이브를 실행하여 메인 로비까지 들어간 뒤 다음 항목을 따라하시면 됩니다.

### 2. ImageMax 창에서 `START` 버튼 클릭

ImageMax 프로그램 창 좌측 하단, `START`(F7) 버튼을 눌러주세요. 스크립트가 시작되고 자동으로 아이템, 장비 목록 UI로 진행하여 갯수를 세줄 것입니다.

### 3. 6~7분 기다리기

데이터를 받아오는게 아닌 이미지 기반의 인식이기때문에 어느정도의 시간이 걸릴 수 있습니다. 라면을 끓이거나 커피를 내려오는 등 할일을 하시면 됩니다.

이미지 인식 중 같은 이미지를 여러번 클릭하는 것은 비슷한 이미지를 2차확인하는 과정입니다.

집계가 끝나면 ImageMax 프로그램 창에서 `script_finished`라는 칸이 선택된 채 30초 뒤 중지됩니다. (딜레이에 별다른 의미는 없습니다)

`script_finished` 칸이 선택되어있거나 `STOP`이라는 메시지가 콘솔에 떠 있다면 완료입니다.

### 4. 완료, 집계된 데이터 확인

`resource_counter/result_data_날짜.json` 로 결과물이 출력됩니다. 다만 이것은 재화 계획관리용 사이트에 등록할 형태의 파일이라 사람이 확인하기에는 무리가 있습니다.

집계한 재화들만이 기록된 파일은 `resource_counter/output.json` 입니다. 이 파일 또한 id로 적혀져있어 사람이 구별하기는 힘들기때문에, 잘 세어졌는지 확인하고싶다면 아래 세 가지 방법 중 하나를 선택하시면 됩니다.

1. `settings.py:DEBUG_SAVE_NAME_REPLACED_RESULT` 플래그를 `True`로 바꿔줍니다.
   - 이 경우 사람이 읽을 수 있는 아이템 이름으로 치환된 디버그 파일을 `resource_counter/debug_output.json`으로 출력해줍니다.
   - 해당 파일의 `Unmanaged` 키는 굳이 확인할 필요 없는 경험치들입니다.
2. 만약 0번에서 본인의 데이터를 가져왔다면, `resource_counter/result_diff_날짜.json` 파일에서 아이템별 변경된 수치를 알 수 있습니다.
   - 이 때 이상할정도로 변경치가 높은 아이템이 있는 경우 `resource_counter/warning_result_diff_날짜.json`에 출력됩니다.
3. 재화 플래너 사이트에 import합니다.
   - 다음 항목에 적힌대로 넣고, 시각화된 자료와 함께 집계된게 맞는지 확인하는 방법입니다.

### 5. 재화 플래너 사이트에 등록

[Justin163's Resource Planner](https://justin163.com/planner/)에 접속해서 하단의 `Transfer` 버튼을 누릅니다.

![_readme_attachment_3_planner_import](https://user-images.githubusercontent.com/2003010/230747763-a1232cf5-f3af-4f2a-9631-6a05ec6cba7c.png)

`Import`버튼을 누른 후 나오는 입력칸에 4번 과정에서 나온 `result_data_날짜.json`의 내용을 복사해 붙여넣어줍니다.

`OK`버튼을 누르면 집계된 데이터가 사이트에 반영됩니다. 사이트 하단의 `Resources`, `Gear` 버튼을 눌러 등록된 재화를 확인할 수 있습니다.

## CAUTION

재화 플래너에서 학생 정보, 이벤트 정보 등을 수정했다면 Usage 0번 항목에 따라 `resource_counter/planner_exported.json` 파일을 덮어씌워주셔야합니다. 덮어씌우시지 않으면 수작업으로 수정한 데이터들이 사라집니다.

학생 레벨, 인연랭크, 스킬, 착용장비 등의 정보는 집계하지 않습니다. 거기까지 구현되지 않았습니다. 이 스크립트는 오직 `보고서, 오파츠, BD, 교본, 비의서, 장비 설계도, 장비 강화석, 전용무기 성장재료` 만을 집계합니다.

본 스크립트는 개인 편의를 목적으로 개발되었으며 캡쳐된 이미지 리소스나 종속성이 있는 프로그램의 권리 문제가 있을 시 언제든지 삭제될 수 있습니다.

## Known Issues

재화 수량 OCR과정에서 `x`와 `2`가 붙어있는경우 종종 오인식이 발생합니다. (i.e. `x225`->`2325`, `x245`->`x2245`) 이런 문제는 1920\*1080 해상도에서 비교적 덜 발생합니다.

한번의 집계에서 0~2건정도 발생하는데 이걸 감지할 수 있는 방법이 추가되기 전까지는 `resource_counter/warning_result_diff_날짜.json`파일에서 이상하게 큰 값이 있었는지 확인해주시면 좋습니다.

[특정 이미지 누락 문제](https://github.com/JGR06/bluearchive-resource-counter/issues/1#issue-1656316884)
- 전용무기 강화재료 스프링/망치/총열 모두 T4(마지막 티어) 이미지가 누락되어있음

[해상도 대응 문제](https://github.com/JGR06/bluearchive-resource-counter/issues/2#issue-1656324645)
- 현재 1920\*1080(280dpi) 해상도와 1600\*900(240dpi) 해상도에서만 동작합니다.
- 캡쳐된 이미지 검색을 통해 작동하는 스크립트로, 해상도와 dpi를 맞춰야 정상적으로 동작합니다.

## Contribution

스크립트에 문제 혹은 의아한점이 있다면 언제든지 수정해서 PR을 보내주시거나, 이슈를 등록해주시면 됩니다.

문제가 발생하여 로그를 확인하고싶으신 경우 프로젝트 최상위 디렉터리에 `Trace` 폴더를 만들면 로그가 저장됩니다. 이 경우 파이썬 스크립트에서 에러가 발생할 경우에도 콘솔 창으로 로그를 보여줍니다.

해당 스크립트를 참고해서 다른 스크립트를 만들거나 하셔도 무방합니다. 프로그램 종속성 문제와 언어 문제로 인해 글로벌 서비스에서는 현재 사용할 수 없기때문에, 직접 테서렉트를 추가해서 사용하시거나 [AutoHotKey](https://www.autohotkey.com/)를 이용해서 구현하시길 추천드리는 바입니다. OCR의 경우 tesseract trainedata를 추가로 긁어오시면 사용할 수 있습니다.

해상도를 추가 등록하고싶으시면 원하시는 해상도에 맞춰 ImageMax에서 캡쳐를 진행하신 뒤, 아래의 파일들을 `./switch_resolution/image_variants/`로 복사해주시면 됩니다.
- `./resource_counter/resource_counter.xml` 를 복사해서 `해상도가로_해상도세로_dpi.xml`로 이름 수정
- `./resource_counter/image/` 폴더를 복사해서 `해상도가로_해상도세로_dpi`폴더로 이름 수정
이렇게 복사하고 올려주시면 추후 같은 해상도를 사용하려는 사용자가 세팅을 복사해올 수 있습니다.

## ETC

개발과정에서 왜 이런 선택들이 있었는지 등 사족이 궁금하시면 `resource_counter/devlog.md` 파일에 기재된 내용을 구경하시면 됩니다.

