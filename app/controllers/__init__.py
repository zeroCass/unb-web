def blueprints():
    from .turmas_controller import bp as turmas_bp
    # from .qrcode_controller import bp as qrcode_bp
    from .aulas_controller import bp as aulas_bp
    from .exames_controller import bp as exames_bp
    from .questoes_controller import bp as questoes_bp
    return [turmas_bp, questoes_bp]
