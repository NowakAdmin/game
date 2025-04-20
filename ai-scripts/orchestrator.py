import os
import sys
import re
import json
import openai

# Ścieżki projektu
SPEC_PATH = os.path.join(os.path.dirname(__file__), "..", "spec", "modules.md")
GAME_DIR = os.path.join(os.path.dirname(__file__), "..", "game")
TEST_DIR = os.path.join(os.path.dirname(__file__), "..", "tests")

# Ustawienie klucza API
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("ERROR: Zmienna środowiskowa OPENAI_API_KEY nie jest ustawiona.")
    sys.exit(1)

PROMPT_TEMPLATE = (
    "Na podstawie specyfikacji modułu {module} w pliku modules.md:\n\n"  
    "{spec_section}\n\n"
    "Wygeneruj dwa pliki w formacie JSON z kluczami:\n"
    "  - \"code\": zawartość pliku {module}.gd (GDScript)\n"
    "  - \"tests\": zawartość pliku test_{module}.gd (testy GUT)\n"
    "Odpowiedź wyłącznie w formacie JSON, bez dodatkowego tekstu."
)


def load_spec_section(module_name: str) -> str:
    """
    Wyciąga fragment specyfikacji oznaczony nagłówkiem '### {ModuleName}'.
    """
    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex na sekcję od ### ModuleName do następnego ### lub ##
    pattern = rf"^###\s+{re.escape(module_name)}[\s\S]*?(?=^###|^##|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        print(f"ERROR: Nie znaleziono sekcji specyfikacji dla modułu '{module_name}' w {SPEC_PATH}.")
        sys.exit(1)
    return match.group(0)


def generate_module(module_name: str, spec_section: str) -> dict:
    """
    Wyślij prompt do OpenAI i zwróć parsowany JSON z kluczami 'code' i 'tests'.
    """
    prompt = PROMPT_TEMPLATE.format(module=module_name, spec_section=spec_section)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Jesteś doświadczonym programistą GDScript w Godot 4."},
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("ERROR: Nie udało się sparsować odpowiedzi AI jako JSON:", e)
        print("Odpowiedź AI:", content)
        sys.exit(1)
    return data


def write_files(module_name: str, data: dict) -> None:
    """
    Zapisuje wygenerowany kod i testy do odpowiednich plików.
    """
    os.makedirs(GAME_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)

    code_path = os.path.join(GAME_DIR, f"{module_name}.gd")
    test_path = os.path.join(TEST_DIR, f"test_{module_name}.gd")

    with open(code_path, 'w', encoding='utf-8') as f:
        f.write(data['code'])
    print(f"Zapisano kod modułu: {code_path}")

    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(data['tests'])
    print(f"Zapisano testy modułu: {test_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <ModuleName>")
        sys.exit(1)

    module_name = sys.argv[1]
    spec_section = load_spec_section(module_name)
    data = generate_module(module_name, spec_section)
    write_files(module_name, data)


if __name__ == "__main__":
    main()
