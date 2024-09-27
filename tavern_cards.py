class Card():

    def __init__(self, card):

        self.spec = card["spec"]

        self.name = card["data"]["name"]

        self.tags = card["data"]["tags"]
    
        # creator check
        self.creator = ":red[! Undentified Creator]" if len(card["data"]["creator"]) == 0 else card["data"]["creator"]

        # creator comment check
        self.creator_comment = ":red[! Empty creator comment]" if card["data"]["creator_notes"] == "" else card["data"]["creator_notes"]
        
        self.prompts = {"system_prompt": 'Empty' if card["data"]['system_prompt'] == "" else card["data"]['system_prompt'],
                        "post_history_instructions": 'Empty' if card["data"]['post_history_instructions'] == "" else card["data"]['post_history_instructions'],
                        "depth_prompt": 'Empty' if card["data"]['extensions']['depth_prompt']['prompt'] == "" else card["data"]['extensions']['depth_prompt']
                                    }
        
        # permanent card content: 
        # name, scenario, description, personality
        self.permanent_content = {'name': False,
                                  'scenario': False,
                                  'description': False,
                                  'personality': False
                                  }
        for key in self.permanent_content.keys():
            if card['data'][key] == "":
                self.permanent_content[key] = "Empty"
            else: self.permanent_content[key] = card['data'][key]

        self.len_permanent = sum([len(value) for value in self.permanent_content.values() if value is not False])

        # temp card content: 
        # initial message, examples, alternate_greetings
        self.temp_content = {"first_mes": card["data"]["first_mes"],
                             "alternate_greetings": False,
                             "mes_example":  card["data"]["mes_example"],
                             }
        
        if card["data"]["alternate_greetings"] == [""]:
            self.temp_content["alternate_greetings"] = False
        elif card["data"]["alternate_greetings"] == []:
            self.temp_content["alternate_greetings"] = False
        else: self.temp_content["alternate_greetings"] = "\n".join([f'## alt\n{alt}' for alt in card["data"]["alternate_greetings"]])

            

        self.len_temporal = sum([len(value) for value in self.temp_content.values() if value is not False])


        # lorebooks
        self.lorebook_name = 'No lorebook' if card['data']["character_book"] is False else card['data']["character_book"]["name"]
        self.lorebook_entries = card['data']["character_book"]["entries"]
        self.num_lb_entries = len(card['data']["character_book"]['entries']) if card['data']["character_book"] else 0
        self.len_lb_entries = sum([len(i['content']) for i in card['data']["character_book"]["entries"]]) if card['data']["character_book"] else 0