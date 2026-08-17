import { useMemo, useState } from 'react'
import './App.css'

const MEAL_TYPES = ['breakfast', 'lunch', 'dinner'] as const
type MealType = (typeof MEAL_TYPES)[number]

const MEAL_ICONS: Record<MealType, string> = {
  breakfast: '☀️',
  lunch: '⛵',
  dinner: '🌙',
}

interface MealEntry {
  id: number
  day: number
  mealType: MealType
  recipeUrl: string
}

interface ShoppingListIngredient {
  name: string
  quantity_to_buy: string
}

interface ShoppingList {
  ingredients: ShoppingListIngredient[]
}

let nextId = 1

function newMeal(day: number, mealType: MealType = 'dinner'): MealEntry {
  return { id: nextId++, day, mealType, recipeUrl: '' }
}

function isValidUrl(value: string): boolean {
  try {
    const url = new URL(value)
    return url.protocol === 'http:' || url.protocol === 'https:'
  } catch {
    return false
  }
}

function Stepper({
  label,
  hint,
  value,
  min,
  max,
  onChange,
}: {
  label: string
  hint: string
  value: number
  min: number
  max: number
  onChange: (value: number) => void
}) {
  return (
    <div className="stepper">
      <div className="stepper-text">
        <span className="stepper-label">{label}</span>
        <span className="stepper-hint">{hint}</span>
      </div>
      <div className="stepper-controls">
        <button
          type="button"
          aria-label={`Decrease ${label}`}
          disabled={value <= min}
          onClick={() => onChange(value - 1)}
        >
          −
        </button>
        <span className="stepper-value">{value}</span>
        <button
          type="button"
          aria-label={`Increase ${label}`}
          disabled={value >= max}
          onClick={() => onChange(value + 1)}
        >
          +
        </button>
      </div>
    </div>
  )
}

function App() {
  const [days, setDays] = useState(3)
  const [people, setPeople] = useState(4)
  const [meals, setMeals] = useState<MealEntry[]>([newMeal(1)])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [shoppingList, setShoppingList] = useState<ShoppingList | null>(null)
  const [checked, setChecked] = useState<Set<number>>(new Set())

  const validMeals = useMemo(
    () => meals.filter((meal) => isValidUrl(meal.recipeUrl.trim())),
    [meals],
  )

  function updateMeal(id: number, patch: Partial<MealEntry>) {
    setMeals((current) =>
      current.map((meal) => (meal.id === id ? { ...meal, ...patch } : meal)),
    )
  }

  function removeMeal(id: number) {
    setMeals((current) => current.filter((meal) => meal.id !== id))
  }

  function addMeal() {
    const lastDay = meals.length > 0 ? meals[meals.length - 1].day : 1
    setMeals((current) => [...current, newMeal(Math.min(lastDay, days))])
  }

  function handleDaysChange(value: number) {
    setDays(value)
    // Keep meal days within the new voyage length
    setMeals((current) =>
      current.map((meal) => (meal.day > value ? { ...meal, day: value } : meal)),
    )
  }

  function toggleIngredient(index: number) {
    setChecked((current) => {
      const next = new Set(current)
      if (next.has(index)) {
        next.delete(index)
      } else {
        next.add(index)
      }
      return next
    })
  }

  async function createShoppingList() {
    setError(null)
    setShoppingList(null)
    setChecked(new Set())
    setLoading(true)
    try {
      const response = await fetch('/api/shopping-list/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          meals: validMeals.map((meal) => ({
            day: meal.day,
            meal_type: meal.mealType,
            recipe_url: meal.recipeUrl.trim(),
            people,
          })),
        }),
      })
      if (!response.ok) {
        throw new Error(`The galley couldn't respond (HTTP ${response.status})`)
      }
      setShoppingList(await response.json())
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went adrift. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-inner">
          <div className="brand">
            <svg
              className="brand-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M12 3v13" />
              <path d="M12 3l6.5 11H5.5z" fill="rgba(255,255,255,0.25)" />
              <path d="M3 19c1.5 1.4 3 2 4.5 2s3-.6 4.5-2 3-2 4.5-2 3 .6 4.5 2" />
            </svg>
            <h1>
              Nautical<span>Meal</span>
            </h1>
          </div>
          <p className="tagline">
            Provision your galley before you set sail — plan the meals, we chart
            the shopping list.
          </p>
        </div>
        <svg
          className="hero-wave"
          viewBox="0 0 1440 70"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <path
            d="M0,40 C240,70 480,10 720,35 C960,60 1200,20 1440,45 L1440,70 L0,70 Z"
            fill="var(--foam)"
          />
        </svg>
      </header>

      <main>
        <section className="card">
          <div className="card-heading">
            <span className="step-badge">1</span>
            <div>
              <h2>The voyage</h2>
              <p>How long are you out at sea, and how many mouths aboard?</p>
            </div>
          </div>
          <div className="steppers">
            <Stepper
              label="Days"
              hint="Length of the cruise"
              value={days}
              min={1}
              max={60}
              onChange={handleDaysChange}
            />
            <Stepper
              label="Crew"
              hint="People on board"
              value={people}
              min={1}
              max={50}
              onChange={setPeople}
            />
          </div>
        </section>

        <section className="card">
          <div className="card-heading">
            <span className="step-badge">2</span>
            <div>
              <h2>The menu</h2>
              <p>Add a recipe link for each meal you plan to cook aboard.</p>
            </div>
          </div>

          <div className="meals">
            {meals.map((meal) => {
              const trimmedUrl = meal.recipeUrl.trim()
              const urlInvalid = trimmedUrl !== '' && !isValidUrl(trimmedUrl)
              return (
                <div className="meal-row" key={meal.id}>
                  <label className="field day-field">
                    <span>Day</span>
                    <select
                      value={meal.day}
                      onChange={(event) =>
                        updateMeal(meal.id, { day: Number(event.target.value) })
                      }
                    >
                      {Array.from({ length: days }, (_, index) => (
                        <option key={index + 1} value={index + 1}>
                          Day {index + 1}
                        </option>
                      ))}
                    </select>
                  </label>

                  <div className="field meal-type-field">
                    <span>Meal</span>
                    <div className="segmented" role="radiogroup" aria-label="Meal type">
                      {MEAL_TYPES.map((type) => (
                        <button
                          key={type}
                          type="button"
                          role="radio"
                          aria-checked={meal.mealType === type}
                          className={meal.mealType === type ? 'active' : ''}
                          onClick={() => updateMeal(meal.id, { mealType: type })}
                        >
                          <span aria-hidden="true">{MEAL_ICONS[type]}</span> {type}
                        </button>
                      ))}
                    </div>
                  </div>

                  <label className="field url-field">
                    <span>Recipe URL</span>
                    <input
                      type="url"
                      placeholder="https://example.com/best-pasta"
                      value={meal.recipeUrl}
                      className={urlInvalid ? 'invalid' : ''}
                      onChange={(event) =>
                        updateMeal(meal.id, { recipeUrl: event.target.value })
                      }
                    />
                  </label>

                  <button
                    type="button"
                    className="remove-btn"
                    aria-label="Remove meal"
                    onClick={() => removeMeal(meal.id)}
                  >
                    ✕
                  </button>
                </div>
              )
            })}
          </div>

          <button type="button" className="add-btn" onClick={addMeal}>
            + Add a meal
          </button>
        </section>

        <div className="launch">
          <button
            type="button"
            className="primary-btn"
            disabled={loading || validMeals.length === 0}
            onClick={createShoppingList}
          >
            {loading ? (
              <>
                <span className="spinner" aria-hidden="true" /> Charting your
                list…
              </>
            ) : (
              <>⚓ Create shopping list</>
            )}
          </button>
          {validMeals.length === 0 && !loading && (
            <p className="launch-hint">Add at least one recipe link to cast off.</p>
          )}
        </div>

        {error && <div className="error-banner">{error}</div>}

        {shoppingList && (
          <section className="card results">
            <div className="card-heading">
              <span className="step-badge">3</span>
              <div>
                <h2>Shopping list</h2>
                <p>
                  Everything the crew of {people} needs for {days}{' '}
                  {days === 1 ? 'day' : 'days'} at sea.
                </p>
              </div>
            </div>
            <ul className="shopping-list">
              {shoppingList.ingredients.map((ingredient, index) => (
                <li key={index}>
                  <label className={checked.has(index) ? 'done' : ''}>
                    <input
                      type="checkbox"
                      checked={checked.has(index)}
                      onChange={() => toggleIngredient(index)}
                    />
                    <span className="ingredient-name">{ingredient.name}</span>
                    <span className="ingredient-qty">
                      {ingredient.quantity_to_buy}
                    </span>
                  </label>
                </li>
              ))}
            </ul>
          </section>
        )}
      </main>

      <footer>
        <p>Fair winds and full bellies ⛵</p>
      </footer>
    </div>
  )
}

export default App
