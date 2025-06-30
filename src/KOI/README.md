# Description for `KOI` Module

This is the main module of the KoiPilot app. It contains the core logic and functionality of the app, and builds up the interface.

---

## `KOI` Module Composition

### `KOI.py`
**Entry Point & Core Logic**  
- Contains the `DesktopKOI` class that initializes the application window
- Handles animation loading and display through `AnimationLoader`
- Implements window dragging functionality and position management
- Manages KOI's mood system with dynamic animation switching

### `Menu.py`
**Interactive Menu System**  
- Implements a fade-in/fade-out animated menu UI
- Provides three core operations:
  - File sorting (calls `FunctionManager.SortFiles`)
  - Name formatting (calls `FunctionManager.FormatNames`)
  - AI chat interface (stubbed)
- Uses canvas-based rounded rectangle rendering for modern visuals

### `FunctionManager.py`
**Business Logic Engine**  
- Central handler for file operations:
  - AI-powered file name formatting
  - Intelligent file sorting with confirmation UI
- Contains threaded execution for long-running operations
- Implements confirmation dialog with:
  - Per-item confirm/cancel buttons
  - Global confirm/cancel all actions
  - Memory-efficient dialog destruction

---

## Supporting Components

### `AnimationLoader.py`
**Animation Resource Management**
- Loads GIF animations with frame extraction
- Returns structured animation dictionaries
- Handles invalid/missing animation folders gracefully

### `Styling.py`
**Visual Style Configuration**