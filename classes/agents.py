def choose_agent(agent):

        agents = {
                'chrome':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'safari':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
                'firefox':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
                'ie':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'opera':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36 OPR/15.0.1147.100'
                }
        
        if agent == "random_agent":
                user_agent = random.choice(agents.keys())
                return user_agent
        elif agent == "chrome":
                user_agent = agents['chrome']
                return user_agent
                
        elif agent == "safari":
                user_agent = agents['safari']
                return user_agent
        elif agent == "firefox":
                user_agent = agents['firefox']
                return user_agent
        elif agent == "internet_explorer":
                user_agent = agents['internet_explorer']
                return user_agent
        elif agent == "opera":
                user_agent = agents['opera']
                return user_agent
                        

