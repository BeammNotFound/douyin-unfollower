from playwright.sync_api import sync_playwright
import time
import os

def save_storage_state(context, file_path='auth.json'):
    """保存登录状态"""
    context.storage_state(path=file_path)
    print(f"登录状态已保存到 {file_path}")

def load_storage_state(file_path='auth.json'):
    """检查是否存在已保存的登录状态"""
    return os.path.exists(file_path)

def unfollow_users():
    with sync_playwright() as p:
        browser_type = p.chromium
        
        # 检查是否有保存的登录状态
        if load_storage_state():
            print("发现已保存的登录状态，尝试使用...")
            browser = browser_type.launch(headless=False)
            context = browser.new_context(storage_state="auth.json")
            page = context.new_page()
        else:
            print("未找到登录状态，需要重新登录...")
            browser = browser_type.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
        
        try:
            # 访问抖音
            page.goto("https://www.douyin.com")
            
            # 如果没有登录状态，等待用户扫码登录
            if not load_storage_state():
                print("请使用抖音APP扫码登录...")
                # 等待登录成功，检测URL变化或特定元素出现
                page.wait_for_selector(".personal-card", timeout=60000)
                print("登录成功！")
                # 保存登录状态
                save_storage_state(context)
            
            # 进入关注列表页面
            print("正在进入关注列表...")
            page.goto("https://www.douyin.com/user/self?from_tab_name=main")
            time.sleep(5) 

            print("等待并点击关注列表标签...")
            # 使用更具体的选择器定位关注标签
            follow_tab = page.wait_for_selector(".C1cxu0Vq", timeout=10000)
            if follow_tab:
                follow_tab.click()
                print("成功点击关注列表标签")
            else:
                print("未找到关注列表标签")
            time.sleep(2)  # 等待页面加载
            
            while True:
                # 获取所有取消关注按钮
                unfollow_buttons = page.query_selector_all("button:has-text('已关注')")
                
                if not unfollow_buttons:
                    print("没有找到更多的关注按钮，任务完成！")
                    break
                
                for button in unfollow_buttons:
                    try:
                        # 点击"已关注"按钮
                        button.click()
                        # time.sleep(1)
                        
                        # 点击确认取消关注的弹窗
                        confirm_button = page.query_selector("button:has-text('取消关注')")
                        if confirm_button:
                            confirm_button.click()
                        
                        print("成功取消一个关注")
                        # time.sleep(2)  
                        
                    except Exception as e:
                        print(f"取消关注时出错: {e}")
                        continue
                
                # 滚动页面加载更多
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(2)
                
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            # 等待一下，让用户看到结果
            time.sleep(5)
            browser.close()

if __name__ == "__main__":
    unfollow_users() 