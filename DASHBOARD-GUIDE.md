# 📊 Dashboard Components Guide

**Complete Guide to Understanding Your AI Worker Productivity Dashboard**

This document describes every component, tab, card, and visualization on the dashboard, explaining what data is displayed and how to interpret it.

---

## 🎯 Dashboard Overview

The **AI Worker Productivity Command Center** is a single-page dashboard (no tabs) that provides real-time monitoring of factory floor operations using AI-detected events from CCTV cameras. All components are visible on one scrollable page for at-a-glance monitoring.

**Dashboard URL:** http://localhost:3000

---

## 📋 Main Components (Top to Bottom)

### 1. **HEADER SECTION** - Command Center Title & Controls

**Location:** Top of dashboard  
**Purpose:** Main navigation and data control

#### Components:

**A. Title Block:**
- **"AI Worker Intelligence"** - Category label
- **"Productivity Command Center"** - Main dashboard title
- **"Live factory telemetry..."** - Description of dashboard purpose

**B. Action Buttons:**

| Button | Function | When to Use |
|--------|----------|-------------|
| **Refresh Data** | Reloads all metrics without clearing database | Check latest updates |
| **Reseed sample data** | Clears and regenerates 24 hours of elite data | Fresh start with realistic patterns |

**C. Error Display:**
- Red alert box appears if backend is unreachable
- Shows connectivity or API errors

---

### 2. **KEY METRICS CARDS** - Factory Overview (4 Cards)

**Location:** Directly below header  
**Purpose:** At-a-glance factory health metrics

#### Card 1: Active Workers
- **Number Displayed:** Count of workers with recent activity
- **Indicator:** 🟢 Pulsing green dot (ELITE feature - shows "live" status)
- **Subtitle:** "with recent activity"
- **What It Means:** How many workers have logged events recently
- **Elite Feature:** Pulsing animation shows system is live and updating

#### Card 2: Active Workstations
- **Number Displayed:** Count of workstations with recent activity
- **Subtitle:** "monitored in real-time"
- **What It Means:** How many workstations have processed events

#### Card 3: Avg Utilization
- **Number Displayed:** Percentage (e.g., "68.3%")
- **Subtitle:** "across workers"
- **What It Means:** Average time workers spend in "working" state vs total time
- **Interpretation:** 
  - >80% = Highly productive
  - 50-80% = Normal operations
  - <50% = Investigate idle time

#### Card 4: Production Rate
- **Number Displayed:** Units per hour (e.g., "2.7")
- **Subtitle:** "units per hour"
- **What It Means:** Average units produced per hour across all workers
- **Interpretation:** Higher = More productive workforce

---

### 3. **WORKER LEADERBOARD** - Top Performer Table

**Location:** Left side, large section  
**Purpose:** Rank workers by utilization percentage

#### Table Columns:

| Column | Data Shown | How to Interpret |
|--------|------------|------------------|
| **Worker** | Worker name/ID (e.g., "Worker 1", "W1") | Identifies the worker |
| **Utilization** | Progress bar + percentage | Visual + numeric productivity |
| **Units** | Units per hour (e.g., "3.65 / hr") | Production speed |
| **Active** | Active time in hours (e.g., "14.2 h") | Total working time |
| **Last Seen** | Timestamp of last event | Recency of activity |

#### Visual Features:

**Progress Bar:**
- 🟢 Full bar = High utilization
- 🟡 Medium bar = Moderate utilization
- 🔴 Short bar = Low utilization

**Color-Coded Percentages (ELITE Feature):**
- **🟢 Emerald (Green):** ≥85% utilization - Excellent performance
- **⚪ White:** 50-84% utilization - Normal performance
- **🟡 Amber (Yellow):** <50% utilization - Needs attention

**Sorting:**
- Always sorted by highest utilization first
- Shows top 8 workers

**What to Look For:**
- Workers consistently at top = Star performers
- Workers at bottom = May need support or training
- Amber percentages = Investigate idle/absent time

---

### 4. **THROUGHPUT PULSE** - Bar Chart + Heatmap

**Location:** Right side, next to leaderboard  
**Purpose:** Visualize productivity patterns

#### A. Units vs Utilization Chart (Bar Chart)

**Chart Type:** Dual-axis bar chart  
**X-Axis:** Worker names  
**Y-Axes:**
- Left: Units/hour (cyan bars)
- Right: Utilization % (purple bars)

**How to Read:**
- **Cyan bars:** How many units each worker produces per hour
- **Purple bars:** What percentage of time worker is active
- **Compare bars:** High purple + high cyan = Ideal (productive AND efficient)

**Insights:**
- High utilization + low units = Working but not producing (investigate)
- Low utilization + high units = Fast but idle often (optimize scheduling)
- Both high = Star performer

#### B. 24-Hour Productivity Heatmap (ELITE Feature)

**Location:** Below the bar chart  
**Purpose:** Show productivity patterns across 24 hours

**How to Read:**
- **Grid:** 24 cells, one for each hour (0-23)
- **Colors:**
  - 🟢 **Emerald:** High productivity (>80%)
  - 🔵 **Cyan:** Moderate productivity (60-80%)
  - 🟡 **Amber:** Low productivity (40-60%)
  - 🔴 **Rose:** Very low productivity (<40%)
- **Opacity:** Darker = more productive, lighter = less productive

**Elite Patterns You'll See:**
- **Hour 6 (6:00 AM):** 🟡 Lighter color - Slow Start pattern (shift warmup)
- **Hour 13 (1:00 PM):** 🔴 Very light - Lunch Dip pattern (productivity drop)
- **Hours 9-11, 14-16:** 🟢 Darker - Peak productivity hours

**Hover:** Shows exact hour and productivity percentage

**Use Case:**
- Identify shift bottlenecks
- Plan maintenance during low-activity hours
- Optimize break schedules

---

### 5. **WORKSTATIONS SECTION** - Station Cards Grid

**Location:** Full width below leaderboard  
**Purpose:** Monitor individual workstation performance

#### Each Card Shows:

**Header:**
- Station name (e.g., "Workstation 1")
- Station ID badge (e.g., "S1")
- Last activity timestamp

**Utilization Bar:**
- Progress bar showing utilization percentage
- Gradient from emerald to cyan

**Metrics:**
- **Left:** Utilization percentage (e.g., "72.5% util")
- **Right:** Throughput rate (e.g., "2.3 u/hr")

**Production Stats (Bottom Box):**
- **Occupancy:** Hours station was in use
- **Production:** Total units produced

**How to Interpret:**

| Metric | What It Means | Healthy Range |
|--------|---------------|---------------|
| Utilization | % of occupied time spent working | >70% |
| Throughput | Units produced per hour | Varies by station type |
| Occupancy | Total time station was active | Should match shift hours |
| Production | Total output | Compare across stations |

**What to Look For:**
- Stations with low utilization = Investigate idle time
- Stations with low throughput = Check equipment/process
- Recent last activity = Station is operational

---

### 6. **AI EVENT STREAM** - Live Event Feed

**Location:** Bottom left, large section  
**Purpose:** Show recent AI-detected events in real-time

#### Event Card Components:

**Top Line:**
- Event type in uppercase (e.g., "WORKING", "IDLE", "PRODUCT COUNT")

**Second Line:**
- Worker ID (e.g., "Worker W1")
- Workstation ID (e.g., "@ S3")

**Right Side:**
- **Time badge:** Event timestamp (e.g., "2:45:32 PM")
- **Confidence badge:** AI confidence score (e.g., "conf 92%")
- **Units badge (product_count only):** Units produced (e.g., "+3 units")

#### Event Type Colors:

| Event Type | Color | What It Means |
|------------|-------|---------------|
| **WORKING** | 🟢 Emerald/Green | Worker actively working |
| **IDLE** | 🟡 Amber/Yellow | Worker present but not working |
| **ABSENT** | 🔴 Rose/Red | Worker not detected at station |
| **PRODUCT COUNT** | 🔵 Cyan/Blue | Units produced detected |

#### Confidence Filter (ELITE Feature):

**Checkbox:** "Hide Low Confidence (<80%)"
- **Unchecked:** Shows all events
- **Checked:** Hides events with confidence <80%

**Why Use It:**
- Filter out unreliable AI detections
- Focus on high-confidence events
- Data quality control

**Event Counter:**
- Shows how many events are displayed (e.g., "42 events")

**Sorting:**
- Newest events at top
- Shows up to 25 most recent events
- Auto-refreshes every 30 seconds

**What to Look For:**
- Frequent "IDLE" events = Worker may need support
- High "PRODUCT COUNT" = Good productivity
- Low confidence scores = Camera/AI may need recalibration

---

### 7. **FACTORY PULSE** - Summary Stats Panel

**Location:** Bottom right  
**Purpose:** Aggregate factory-wide statistics

#### Components:

**A. Productive Time Card**
- **Number:** Total productive hours across all workers
- **Progress Bar:** Visual representation of utilization
- **Subtitle:** "Aggregate productive time across all workers"
- **What It Means:** Sum of all working hours

**B. Total Production Card**
- **Number:** Total units produced
- **Subtitle:** "Across monitored workstations"
- **What It Means:** Factory's total output in the time window

**C. Time Window Card**
- **Start Date/Time:** Beginning of measurement period
- **End Date/Time:** End of measurement period
- **What It Means:** The time range for all displayed metrics

**D. Seed Prompt Card (Cyan)**
- **Title:** "Need fresh telemetry?"
- **Description:** Explains seeding functionality
- **Button:** "Seed without clearing"
- **Purpose:** Add more data without deleting existing

**When to Use:**
- Click "Seed without clearing" to add more sample events
- Useful for demos or testing with more data
- Does not delete existing events

---

## 🔄 AUTO-REFRESH FEATURE (ELITE)

**Interval:** Every 30 seconds  
**What Refreshes:**
- All metrics cards
- Worker leaderboard
- Workstation cards
- Event stream
- Factory pulse

**Visual Indicator:**
- Pulsing green dot on "Active Workers" card shows live status

**Manual Refresh:**
- Click "Refresh Data" button for immediate update

---

## 🎨 DESIGN FEATURES

### Color Scheme:
- **Background:** Dark slate/indigo gradient (modern dashboard aesthetic)
- **Cards:** Translucent white with blur effect (glassmorphism)
- **Accents:** Cyan, emerald, amber, rose (status indicators)

### Animations:
- **Fade-in:** Components slide up and fade in on load
- **Pulse:** Green "live" indicator pulses every 2 seconds
- **Hover:** Cards and table rows highlight on hover
- **Smooth Transitions:** All state changes are animated

### Accessibility:
- Color-coded AND text-labeled (not relying on color alone)
- Clear labels and descriptions
- Hover tooltips on heatmap
- Readable contrast ratios

---

## 📊 INTERPRETING THE DASHBOARD

### Healthy Factory Indicators:
✅ Average utilization >70%  
✅ Most workers in emerald/white zones (not amber)  
✅ Consistent production across workstations  
✅ High confidence events (>85%)  
✅ Regular "working" and "product_count" events  
✅ Heatmap shows expected patterns (lunch dip, peak hours)  

### Warning Signs:
⚠️ Average utilization <50%  
⚠️ Many workers in amber zone  
⚠️ Workstations with 0 production  
⚠️ Low confidence events (<75%)  
⚠️ Frequent "absent" events  
⚠️ Heatmap shows unexpected low productivity  

### Investigation Needed:
🔴 No active workers  
🔴 0 production across factory  
🔴 All events showing "idle" or "absent"  
🔴 Very low confidence scores (<60%)  
🔴 Backend connectivity errors  

---

## 🎯 ELITE FEATURES SUMMARY

The dashboard includes 8 elite features that distinguish it from standard implementations:

### 1. **Pulsing Live Indicator**
- **Location:** Active Workers card
- **Visual:** Green dot with scale/opacity animation
- **Purpose:** Shows dashboard is live and updating

### 2. **Lunch Dip Pattern**
- **Location:** Visible in heatmap hour 13
- **Pattern:** Productivity drops 1:00-1:45 PM
- **Purpose:** Realistic factory lunch break simulation

### 3. **Slow Start Pattern**
- **Location:** Visible in heatmap hour 6
- **Pattern:** Lower productivity 6:00-6:30 AM
- **Purpose:** Realistic shift startup warmup period

### 4. **Product Correlation**
- **Location:** Event stream
- **Logic:** Product counts ONLY during "working" events
- **Purpose:** Enforces realistic data - no production during idle/absent

### 5. **24-Hour Heatmap**
- **Location:** Right panel below bar chart
- **Visual:** 24-cell grid with color intensity
- **Purpose:** Visual timeline of hourly productivity patterns

### 6. **Color-Coded Thresholds**
- **Location:** Worker leaderboard utilization column
- **Colors:** Amber (<50%), White (50-84%), Emerald (≥85%)
- **Purpose:** At-a-glance performance assessment

### 7. **Auto-Refresh**
- **Interval:** 30 seconds
- **Scope:** All dashboard data
- **Purpose:** Real-time monitoring experience

### 8. **Confidence Filter**
- **Location:** Event stream section
- **Control:** Checkbox toggle
- **Purpose:** Data quality control - hide unreliable events

---

## 🔧 DASHBOARD ACTIONS

### Primary Actions:

| Button/Control | Location | Effect |
|----------------|----------|--------|
| **Refresh Data** | Header | Reload all metrics (no DB changes) |
| **Reseed sample data** | Header | Clear DB and generate 24hrs elite data |
| **Seed without clearing** | Factory Pulse panel | Add more data keeping existing |
| **Hide Low Confidence** | Event Stream | Filter events <80% confidence |

### When to Use Each:

**Refresh Data:**
- After making backend changes
- To see latest updates
- Checking if new events arrived

**Reseed sample data:**
- First time setup
- Want fresh elite patterns
- Demonstrating all features
- Testing with clean slate

**Seed without clearing:**
- Want more events for testing
- Keeping existing data
- Incremental data addition

**Hide Low Confidence:**
- Focus on reliable detections
- Reduce noise in event stream
- Quality analysis

---

## 📱 RESPONSIVE DESIGN

The dashboard adapts to different screen sizes:

- **Desktop (>1024px):** Full 3-column layout
- **Tablet (768-1024px):** 2-column layout
- **Mobile (<768px):** Single column stacked

All components remain functional across all sizes.

---

## 🎓 ADVANCED INSIGHTS

### Reading Worker Patterns:

**Consistent High Performer:**
- Always in top 3 of leaderboard
- Emerald utilization color
- High units per hour
- Minimal idle time

**Needs Support:**
- Bottom of leaderboard
- Amber utilization color
- Low units per hour
- Frequent idle/absent events

**Equipment Issue:**
- High utilization but low units
- Suggests slow equipment
- Check workstation throughput

### Reading Factory Patterns:

**Well-Optimized Factory:**
- Heatmap shows clear peaks and valleys
- Lunch dip visible (expected)
- Slow start visible (expected)
- Production distributed across stations

**Scheduling Issue:**
- Heatmap shows unexpected low hours
- Uneven workstation utilization
- Many workers idle during expected peak

**Data Quality Issue:**
- Many low confidence events
- Erratic heatmap patterns
- Inconsistent worker metrics

---

## 🚀 QUICK REFERENCE

### Dashboard Sections (Top to Bottom):
1. Header + Key Metrics (4 cards)
2. Worker Leaderboard (left) + Throughput Pulse (right)
3. Workstations Grid (full width)
4. Event Stream (left) + Factory Pulse (right)

### Key Numbers to Monitor:
- **Average Utilization:** Should be >70%
- **Active Workers:** Should match shift size
- **Production Rate:** Compare to targets
- **Event Confidence:** Most should be >85%

### Elite Features at a Glance:
- 🟢 Pulsing dot = Live status
- 🌈 Color codes = Performance zones
- 🔥 Heatmap = Hourly patterns
- ✅ Filter = Data quality control

---

## 📚 RELATED DOCUMENTATION

For deeper technical details, see:
- **README.md** - Complete project guide
- **ELITE-UPGRADE.md** - Elite features implementation
- **API-DOCS.md** - Backend API reference
- **OPTIMIZATION-REPORT.md** - Code quality details

---

**Dashboard Version:** 2.0 Elite  
**Last Updated:** January 21, 2026  
**Access:** http://localhost:3000  
**API Docs:** http://localhost:8000/docs  

Made with ❤️ for clarity and usability.
