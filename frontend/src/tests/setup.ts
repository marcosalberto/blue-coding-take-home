import "@testing-library/jest-dom/vitest"

Object.defineProperty(window, "matchMedia", {
    value: vi.fn(() => ({ matches: true, addListener: vi.fn(), removeListener: vi.fn() }))
});