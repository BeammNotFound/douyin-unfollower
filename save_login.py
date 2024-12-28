from playwright.sync_api import sync_playwright

def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 访问抖音
            print("正在打开抖音...")
            page.goto("https://www.douyin.com")
            
            # 等待用户确认已登录
            input("请确认你已经登录成功，然后按回车键继续...")
            
            # 保存登录状态
            context.storage_state(path="auth.json")
            print("登录状态已保存到 auth.json")
            
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    save_login_state() 