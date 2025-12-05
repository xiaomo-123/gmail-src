from bit_api import *
import time
import asyncio
import random
from playwright.async_api import async_playwright, Playwright
import io
from PIL import Image

#googurl='https://support.google.com/accounts/answer/27441?hl=zh-Hans&co=GENIE.Platform%'
googurl='https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default'

# 全局变量定义
surnames = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"]
names = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英", "霞", "平"]
surname_map = {"张": "zhang", "王": "wang", "李": "li", "赵": "zhao", "刘": "liu", "陈": "chen",
             "杨": "yang", "黄": "huang", "周": "zhou", "吴": "wu", "徐": "xu", "孙": "sun",
             "马": "ma", "朱": "zhu", "胡": "hu", "郭": "guo", "何": "he", "高": "gao",
             "林": "lin", "罗": "luo"}
name_map = {"伟": "wei", "芳": "fang", "娜": "na", "敏": "min", "静": "jing", "丽": "li",
          "强": "qiang", "磊": "lei", "军": "jun", "洋": "yang", "勇": "yong", "艳": "yan",
          "杰": "jie", "娟": "juan", "涛": "tao", "明": "ming", "超": "chao", "秀英": "xiuying",
          "霞": "xia", "平": "ping"}
punctuations = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', ':', ';', '<', '>', '?', '/']
gerenfullxpath='/html/body/div[2]/div/div[1]/section/div/div[1]/article/section/div/div[1]/div/div[3]/a[1]'
xingfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/input'
namefullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/input'
nextfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button/span'

yearfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div[3]/div/div[1]/div[1]/div/div[1]/input'

monthfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div[1]/div/div[1]/div/div[1]/div'

dayfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/input'

sexfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div[1]/div/div[1]/div'
next2fullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button/div[3]'
emailfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]'

emailinputfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[1]/div[1]/div/div[1]/input'
next3fullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button/div[3]'

passwdfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'
repasswdfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'


next4fullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button/span'
next5fullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button/span'

erfullxpath='/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section[1]/div/div/div/div/img'
async def run(playwright: Playwright):
    browser_ids = getBrowserIds()
    browser_id=browser_ids[1]  
    
    # browser_id = createBrowser()   
    
    print("browser_ids ==>>> ", browser_id)
    update_proxy_for_single_window(browser_id) 
    res = openBrowser(browser_id)
    # 检查响应结构，确保有data和ws键
    if not isinstance(res, dict):
        print(f"错误：openBrowser返回的不是字典: {res}")
        return
        
    if 'data' not in res:
        print(f"错误：响应中没有'data'键: {res}")
        return
        
    if not isinstance(res['data'], dict):
        print(f"错误：res['data']不是字典: {res['data']}")
        return
        
    if 'ws' not in res['data']:
        print(f"错误：res['data']中没有'ws'键: {res['data']}")
        return
        
    ws = res['data']['ws']
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    print('new page and goto baidu')

    page = await default_context.new_page()
    await page.goto(googurl)
    await handle_script(page)
async def handle_script(page):
    # 等待xingfullxpath元素出现并点击
    print("等待姓输入框出现...")
    await page.wait_for_selector(f"xpath={xingfullxpath}", timeout=10000)
    await page.click(f"xpath={xingfullxpath}")

    # 随机生成姓
    random_surname = random.choice(surnames)
    await page.fill(f"xpath={xingfullxpath}", random_surname)
    print(f"已输入姓: {random_surname}")
    
    # 等待namefullxpath元素出现并点击
    print("等待名输入框出现...")
    await page.wait_for_selector(f"xpath={namefullxpath}", timeout=10000)
    await page.click(f"xpath={namefullxpath}")

    # 随机生成名
    random_name = random.choice(names)
    await page.fill(f"xpath={namefullxpath}", random_name)
    print(f"已输入名: {random_name}")
    time.sleep(2)
    await page.click(f"xpath={nextfullxpath}")
    print("等待年份框出现...")
    await page.wait_for_selector(f"xpath={yearfullxpath}", timeout=10000)
    await page.click(f"xpath={yearfullxpath}")

    # 在输入框中随机输入1985或1999
    random_year = random.choice([1985, 1999])
    await page.wait_for_selector(f"xpath={yearfullxpath}", timeout=5000)
    await page.fill(f"xpath={yearfullxpath}", str(random_year))
    print(f"已选择年份: {random_year}")

    # 等待月份下拉框出现并随机选择
    print("等待月份下拉框出现...")
    await page.wait_for_selector(f"xpath={monthfullxpath}", timeout=10000)
    await page.click(f"xpath={monthfullxpath}")

    # 随机选择1-12月
    month = random.randint(1, 12)
    month_option = f"//li[@data-value='{month}']"
    await page.wait_for_selector(f"xpath={month_option}", timeout=5000)
    await page.click(f"xpath={month_option}")
    print(f"已选择月份: {month}")

    # 等待日期输入框出现
    print("等待日期输入框出现...")
    await page.wait_for_selector(f"xpath={dayfullxpath}", timeout=10000)
    await page.click(f"xpath={dayfullxpath}")

    # 随机选择1-28日(确保所有月份都有)
    day = random.randint(1, 28)
    await page.wait_for_selector(f"xpath={dayfullxpath}", timeout=5000)
    await page.fill(f"xpath={dayfullxpath}", str(day))
    print(f"已输入日期: {day}")

    # 等待性别下拉框出现并随机选择
    print("等待性别下拉框出现...")
    await page.wait_for_selector(f"xpath={sexfullxpath}", timeout=10000)
    await page.click(f"xpath={sexfullxpath}")

    # 随机选择性别 (1为男性，2为女性)
    gender = random.choice([1, 2])
    gender_text = "Male" if gender == 1 else "Female"
    # 使用文本内容定位性别选项
    gender_option = f"//li[.//span[text()='{gender_text}']]"
    await page.wait_for_selector(f"xpath={gender_option}", timeout=5000)
    await page.click(f"xpath={gender_option}")
    print(f"已选择性别: {gender_text}")
    time.sleep(2)
    await page.click(f"xpath={next2fullxpath}")

 

    print("等待邮箱选择元素出现...")
    try:
        # 使用asyncio.wait同时等待两种元素，哪个先出现就处理哪个
        radio_task = asyncio.create_task(page.wait_for_selector('div[role="radiogroup"]', timeout=10000))
        input_task = asyncio.create_task(page.wait_for_selector(f"xpath={emailinputfullxpath}", timeout=10000))

        done, pending = await asyncio.wait(
            [radio_task, input_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        # 取消未完成的任务
        for task in pending:
            task.cancel()

        # 检查哪个任务先完成
        if radio_task in done:
            # 处理单选按钮组
            radiogroup = radio_task.result()
            print("检测到单选按钮组控件")

            # 获取所有单选按钮
            radio_buttons = await radiogroup.query_selector_all('input[type="radio"]')
            print(f"找到 {len(radio_buttons)} 个单选按钮")

            # 获取所有包含@gmail.com的单选按钮
            gmail_radios = []
            for i, radio in enumerate(radio_buttons):
                # 获取aria-labelledby属性
                label_id = await radio.get_attribute('aria-labelledby')
                text_element = ''
                if label_id:
                    # 获取关联的文本元素
                    label_element = await page.query_selector(f'#{label_id}')
                    if label_element:
                        text_element = await label_element.text_content()

                print(f"单选按钮 {i+1}: {text_element}")

                # 如果文本包含@gmail.com，添加到列表
                if text_element and "@gmail.com" in text_element:
                    gmail_radios.append((radio, text_element))

            # 随机选择一个包含@gmail.com的单选按钮并点击
            if gmail_radios:
                selected_radio, selected_text = random.choice(gmail_radios)
                await selected_radio.click()
                print(f"已随机选择并点击包含@gmail.com的单选按钮: {selected_text}")
                time.sleep(2)
                await page.click(f"xpath={next3fullxpath}")

                # 处理密码输入
                await handle_password_input(page, selected_text.split("@")[0] + "@gmail.com")
                time.sleep(2)
                await page.click(f"xpath={next4fullxpath}")
              
            else:
                print("未找到包含@gmail.com的单选按钮")
        else:
            # 处理邮箱输入框
            email_input = input_task.result()
            print("检测到邮箱输入框控件")
            # 生成邮箱内容：姓名转英文 + 年月日 + 2个英文标点 + 4位数字

            # 获取对应拼音，如果不在映射表中则使用原字符
            surname_en = surname_map.get(random_surname, random_surname)
            name_en = name_map.get(random_name, random_name)
            name_english = f"{surname_en}{name_en}".lower()
            # 年月日
            date_str = f"{random_year}{month}{day}"
            # 使用点号作为分隔符
            random_punctuations = '.'
            # 随机4位数字
            random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            # 组合邮箱内容
            email_content = f"{name_english}{date_str}{random_punctuations}{random_digits}"
            await email_input.click()
            await email_input.fill(email_content)
            print(f"已输入邮箱内容: {email_content}")

            # 生成完整邮箱地址
            full_email = f"{email_content}@gmail.com"

            # 点击下一步按钮
            await page.click(f"xpath={next3fullxpath}")

            # 处理密码输入
            await handle_password_input(page, full_email)
            time.sleep(2)
            await page.click(f"xpath={next5fullxpath}")
            # 处理二维码
          
    except Exception as e:
        print(f"检查邮箱元素时出错: {e}")

    # 等待密码输入完成
    time.sleep(1000)

    print('clsoe page and browser')
    await page.close()

    time.sleep(2)
    closeBrowser(browser_id)


async def get_phone_number_from_api():
    """通过API获取手机号码的函数
    
    返回:
        str: 手机号码，如果获取失败则返回None
    """
    try:
        # 这里需要根据实际的API实现获取手机号码的逻辑
        # 示例代码，需要替换为实际的API调用
        
        # 假设有一个手机号码API端点
        api_url = "https://api.example.com/phone-number"  # 替换为实际的API URL
        
        # 使用requests或其他HTTP客户端调用API
        import requests
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            phone_number = data.get("phone_number")
            if phone_number:
                print(f"成功从API获取手机号: {phone_number}")
                return phone_number
            else:
                print("API返回的数据中没有手机号码")
                return None
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"调用API获取手机号时出错: {e}")
        return None


async def handle_password_input(page, email):
    """处理密码输入并保存账号信息到文件"""
    try:
        # 等待密码输入框出现
        print("等待密码输入框出现...")
        await page.wait_for_selector(f"xpath={passwdfullxpath}", timeout=10000)
        await page.click(f"xpath={passwdfullxpath}")
        
        # 生成密码：姓名字母、年月日数字和英文随机两个符号
        # 获取之前生成的姓名和日期信息
        surname_en = surname_map.get(random.choice(surnames), "zhang")
        name_en = name_map.get(random.choice(names), "wei")
        name_english = f"{surname_en}{name_en}".lower()
        
        # 随机年月日
        year = random.randint(1980, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date_str = f"{year}{month:02d}{day:02d}"
        
        # 随机两个英文符号
        random_punctuations = ''.join(random.sample(punctuations, 2))
        
        # 组合密码
        password = f"{name_english}{date_str}{random_punctuations}"
        
        # 输入密码
        await page.fill(f"xpath={passwdfullxpath}", password)
        print(f"已输入密码: {password}")
        
        # 等待确认密码输入框出现
        print("等待确认密码输入框出现...")
        await page.wait_for_selector(f"xpath={repasswdfullxpath}", timeout=10000)
        await page.click(f"xpath={repasswdfullxpath}")
        
        # 再次输入密码
        await page.fill(f"xpath={repasswdfullxpath}", password)
        print("已确认密码")
        
        # 将邮箱和密码保存到文件
        save_account_to_file(email, password)
        
    except Exception as e:
        print(f"处理密码输入时出错: {e}")

def save_account_to_file(email, password):
    """将邮箱和密码保存到账号txt文件中"""
    try:
        with open("账号.txt", "a", encoding="utf-8") as f:
            f.write(f"{email},{password}\n")
        print(f"账号信息已保存: {email},{password}")
    except Exception as e:
        print(f"保存账号信息时出错: {e}")

async def main():
    async with async_playwright() as playwright:
      await run(playwright)

asyncio.run(main())