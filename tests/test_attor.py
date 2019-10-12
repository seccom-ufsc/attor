from pathlib import Path
from attor import (
    attenders_from_class,
    retrieve_attenders,
    data_from_csv,
    convert,
    Attender,
    Class,
    Student,
)

SEMESTER = '20192'
EXPECTED_NAMES = [
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


def test_retrieve_from_xlsx():
    attenders = retrieve_attenders(
        Path('tests/assets/Presenças/Minicursos/0930/Matutino.xlsx')
    )

    names = sorted(
        attender.name
        for attender in attenders
        if attender.attended
    )

    assert names == EXPECTED_NAMES


def test_no_errors_on_conversion():
    convert(
        Path('tests/assets/Presenças/Minicursos/0930/Matutino.xlsx'),
        Path('tests/generated/Presenças/Minicursos/0930/Matutino.csv'),
    )


def test_fetch_class():
    attenders = attenders_from_class(
        Path('tests/generated/Presenças/Minicursos/0930/Matutino.csv'),
        Path(f'tests/assets/turmas/{SEMESTER}/INE5417/04208A.csv')
    )

    names = sorted(attender.name for attender in attenders)

    assert names == ['Enzo Albornoz', 'Wesly Ataide']


def test_infer_student_type_from_csv():
    assert all(
        isinstance(value, Student)
        for value in data_from_csv(
            Path('tests/generated/Presenças/Minicursos/0930/Matutino.csv')
        )
    )


def test_infer_attender_type_from_csv():
    assert all(
        isinstance(value, Attender)
        for value in data_from_csv(
            Path(f'tests/assets/turmas/{SEMESTER}/INE5417/04208A.csv')
        )
    )


def test_retrieve_from_csv():
    attenders = data_from_csv(
        Path('tests/assets/Presenças/Minicursos/0930/Matutino.csv')
    )

    names = sorted(
        attender.name
        for attender in attenders
        if attender.attended
    )

    assert names == EXPECTED_NAMES
