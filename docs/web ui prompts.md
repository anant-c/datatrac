# DataTrac Design Guide

This document defines the design system for **DataTrac Dataset Registry** so it can be applied consistently across multiple Flask templates.

---

## 🎨 Theme

* **Mode:** Light/Dark toggle (user can switch)
* **Style:** Minimal & clean, with whitespace and simple UI elements
* **Font:** `Inter`, `Roboto`, or system sans-serif fallback
* **Colors:**

  * **Light Mode:**

    * Background: `#f9fafb`
    * Text: `#111827`
    * Card/Table background: `#ffffff`
    * Border: `#e5e7eb`
    * Primary (buttons/links): `#3b82f6` (blue)
    * Danger (delete): `#ef4444`
  * **Dark Mode:**

    * Background: `#1f2937`
    * Text: `#f9fafb`
    * Card/Table background: `#111827`
    * Border: `#374151`
    * Primary: `#60a5fa`
    * Danger: `#f87171`

---

## 📐 Layout

* **Header:** Fixed top header with page title.
* **Sections:** Each section (Upload, Datasets List) styled as a **card** with padding, rounded corners, and subtle shadows.
* **Spacing:** Use consistent margin/padding (`1rem – 2rem`).
* **Alignment:** Centered max-width container (around `900px`).

---

## 📂 Upload Section

* File input styled as a **drag-and-drop box** with dashed border, hover effect, and clickable area.
* Secondary text input (Source URL) styled as minimal input with focus outline.
* Submit button uses **primary color** with hover + active states.

---

## 📊 Dataset Table

* **Table Style:**

  * Full-width, clean borders, subtle row striping.
  * Hover effect: row background highlight.
  * Rounded top corners on header.
* **Columns:** Name, Hash, Source, Created At, Actions.
* **Actions:** Styled as text links (View, Download) and a red button for Delete.
* **Pagination/Filters:** Recommended for larger datasets (optional).

---

## 🌙 Dark Mode

* Implemented with a `.dark-mode` class on `<body>`.
* All background/text colors flip according to theme rules.
* Buttons/links adapt primary/danger colors for dark theme.

---

## ✨ Interactivity

* **Buttons:** Rounded (`border-radius: 0.5rem`), with hover shadows.
* **Transitions:** Smooth (`transition: all 0.2s ease-in-out`).
* **Dark/Light Toggle:** Small button (top-right of header) to switch themes.

---

## ✅ Summary

The design is **minimal, clean, modern** with light/dark theme toggle, card-based layout, interactive tables, and drag-and-drop file upload. This system should be applied consistently across all pages of DataTrac.
