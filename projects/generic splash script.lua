function main(splash, args)
            splash.private_mode_enabled=false
            --[[Method1
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
            --]]
            --[[Method2 
            headers={
                ['User_agent']="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            }
            splash:set_custom_headers(headers)
            --]]
            --Method3
            splash: on_request(function(request)
                request:set_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
                end)
            --#Pass the url as an argument
            url= args.url
            --#Open the website
            assert(splash:go(url))
            --#Wait for it load
            assert(splash:wait(3))
            input_box=assert(splash:select("#search_form_input_homepage"))
            input_box:focus()
            input_box:send_text("my user agent")
            assert(splash:wait(1))
            --[[
            btn=assert(splash:select("#search_button_homepage"))
            btn:mouse_click()
            --]]
            input_box:send_keys("<Enter>")
            assert(splash:wait(2))
            splash:set_viewport_full()
            return {
                --#return png
                image= splash:png(),
                --#return html
                html= splash:html()  
            }
    
        end