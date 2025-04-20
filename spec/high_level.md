## 1. Cel projektu

Stworzenie strategicznej gry osadniczej osadzonej w czasach Bizancjum, działającej na Windows i Android, z minimalistyczną grafiką, w pełni generowanej przez AI.

## 2. Platformy i technologie

- **Silnik gry:** Godot 4.x (GDScript)
- **Język skryptowy:** GDScript (z możliwością C# w przyszłości)
- **Repozytorium:** [https://github.com/NowakAdmin/game](https://github.com/NowakAdmin/game)
- **Orkiestrator AI:** Python 3.10 + OpenAI API (prompt-driven codegen)
- **CI/CD:** GitHub Actions (pipeline generacji, testów i buildów)
- **Wektorowe RAG:** Pinecone / Weaviate (opcjonalnie)

## 3. Struktura katalogów

```
/game/                   # AI-generated kod gry (moduły)
/spec/                   # Dokumentacja specyfikacji (moduły, interfejsy)
/ai-scripts/             # Orchestrator do generacji kodu z OpenAI
/ci/                     # Konfiguracje CI/CD (GitHub Actions)
/tests/                  # Testy jednostkowe GUT dla każdego modułu
/assets/                 # Assety minimalistycznej grafiki (SVG/pixel)
```

## 4. Styl wizualny

- Minimalistyczna, ograniczona paleta 3–4 kolorów
- Siluety budynków, flat design UI
- Wektory (SVG) lub pixel art (64×64–128×128 px)

## 5. Core Gameplay & MVP

**MVP**:

- Dwa surowce: drewno, kamień
- Jeden budynek: tartak (trzy poziomy rozwoju)
- Podstawowy HUD: wyświetlanie zasobów i przycisk budowy
- System populacji: prosty licznik mieszkańców i zadowolenia

## 6. Główne moduły

### ResourceManager

- **Klasa:** ResourceManager
- **Właściwości wewnętrzne:**
  - `resources: Dictionary<String, int>` – przechowuje aktualny stan zasobów (np. „wood”: 100, „stone”: 50)
- **Metody:**
  - `add_resource(type: String, amount: int)`: Dodaje `amount` do zasobu `type`. Jeśli zasób nie istniał, tworzy nowy wpis.
  - `consume_resource(type: String, amount: int) → bool`: Próbuje pobrać `amount` z zasobu `type`. Jeśli dostępne zasoby są wystarczające, zmniejsza stan, emituje sygnał `resource_changed` i zwraca `true`; jeśli nie, emituje sygnał `insufficient_resource` i zwraca `false`.
  - `get_amount(type: String) → int`: Zwraca aktualny stan zasobu `type` (0, jeśli zasób nie istnieje).
- **Sygnały (signals):**
  - `resource_changed(type: String, new_amount: int)` – wyzwalany po każdej udanej zmianie zasobu.
  - `insufficient_resource(type: String, requested: int, available: int)` – wyzwalany w przypadku próby zużycia zbyt dużej ilości.
- **Testy GUT:**
  - `TestAddResource` – weryfikuje, że `add_resource` poprawnie zwiększa stan zasobu i emituje `resource_changed`.
  - `TestConsumeResourceSuccess` – sprawdza, że przy wystarczających zasobach `consume_resource` zwraca `true`, zmienia stan i emituje `resource_changed`.
  - `TestConsumeResourceFailure` – sprawdza, że przy niewystarczających zasobach `consume_resource` zwraca `false` i emituje `insufficient_resource`, bez zmiany stanu.
  - `TestGetAmount` – weryfikuje poprawny zwrot stanu zasobu.

### BuildingSystem

- **Interfejs:** `build(type: String, tier: int)`, `upgrade(building_id: int)`

### UIHUD

- **Interfejs:** Wyświetlanie zasobów, przyciski budowy, okno statusu budynku

### PopulationManager

- **Interfejs:** Zarządzanie liczbą mieszkańców, obliczanie zadowolenia

### EventSystem

- **Interfejs:** Rejestracja i wyzwalanie dynamicznych zdarzeń historycznych

## 7. Orkiestrator AI. Orkiestrator AI

- **Prompt modularny:** każdy moduł opisany w `/spec/modules.md`
- **Skrypt:** `ai-scripts/orchestrator.py` ładuje spec, wysyła prompt, zapisuje plik `.gd`
- **Testy:** AI generuje kod + testy GUT dla każdego modułu

## 8. Harmonogram pierwszych kroków

1. Uzupełnić spec modułów w `/spec/modules.md`
2. Skonfigurować OpenAI API w Pythonie (zainstalować `openai`):
   ```bash
   pip install openai
   ```
3. Przygotować pierwszy prompt i wygenerować `resource_manager.gd` wraz z testami
4. Uruchomić testy GUT i poprawić spec/prompty

## 9. Skalowalność i przyszłość

- Dodanie kolejnych surowców, budynków i drzewka technologicznego
- Rozszerzenie RAG o indeksowanie kodu i specyfikacji
- CI: automatyczna regeneracja kodu po zmianie spec
- Integracja z Discordem do zbierania feedbacku



