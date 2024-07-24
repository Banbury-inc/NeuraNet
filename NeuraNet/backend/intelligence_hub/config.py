class Config:
    # General
    DEBUG = True
    TESTING = False
    prompt_as_command_line_argument = False
    max_tokens = 50 # (Default: 128, -1 = infinite generation, -2 = fill context)
    show_agent_dialogue = False
    use_task_management_agent = False
    use_critic_agent = False
    critic_rating_threshold = 9 # (Default: 9) Between 0-10


    run_squad_benchmark = True


