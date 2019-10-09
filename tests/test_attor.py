from pathlib import Path
from attor import retrieve_attenders, Class


def test_retrieve_who_attended():
    expected_names = [
        'Alan Lüdke',
        'Alexandre Muller Junior',
        'André William Régis',
        'Arthur Philippi Bianco',
        'Arthur Pickcius',
        'Bruna Pagliosa',
        'Bruno Pamplona Huebes',
        'César Cunha',
        'Eduardo Moraes',
        'Enzo Albornoz',
        'Felipe Luiz',
        'Gabriel Baiocchi De Sant\'Anna',
        'Gabriel Oliveira Reis',
        'Gabriel Rosa Costa Giacomoni Pes',
        'Gabriel Simonetto',
        'Gabriel Wesz Machado Oliveira',
        'Guilherme Xavier Souza',
        'Gustavo Emanuel Kundlatsch',
        'Hans Buss Heidemann.',
        'Henrique Webber Andriolo',
        'Hermelan David Kobiahouila Nsonde',
        'Johann Soretz',
        'João Pedro Scremin Ramos',
        'Juan Méndez',
        'Julien Hervot De Mattos Vaz',
        'Keylla Signorelli',
        'Lucas Costa Valença',
        'Lucas Henrique Gonçalves Wodtke',
        'Lucas Tonussi',
        'Marcelo Contin',
        'Pedro Queiroz',
        'Rafael Plentz Lopes',
        'Raphael Ramos Da Silva',
        'Samuel Vieira',
        'Shirley Flores',
        'Teo Haeser Gallarza',
        'Thaina Helena Da Silva',
        'Vinicius Pizetta De Souza',
        'Wesly Ataide',
    ]

    attendances = retrieve_attenders(
        Path('tests/assets/Presenças/Minicursos/0930/Matutino.xlsx')
    )

    names = sorted(
        attender.name
        for attender in attendances
        if attender.attended
    )

    assert names == expected_names
