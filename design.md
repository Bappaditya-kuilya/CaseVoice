---
version: alpha
name: Huly Neon Dark
description: A high-contrast product marketing system with luminous neon accents, dense UI chrome, and a futuristic open-source tone.
colors:
  primary: "#5683DA"
  primary-strong: "#6C90F0"
  secondary: "#D1D1D1"
  tertiary: "#5A250A"
  neutral: "#F6F6F6"
  surface: "#0B0C0F"
  surface-2: "#17181B"
  on-surface: "#FFFFFF"
  on-surface-muted: "#B8BCC6"
  border: "#E5E7EB"
  border-strong: "#FFFFFF1A"
  accent-glow: "#7D5CFF"
  accent-warm: "#FF8A3D"
  error: "#E85D5D"
typography:
  headline-display:
    fontFamily: Esbuild
    fontSize: 84px
    fontWeight: 600
    lineHeight: 101px
    letterSpacing: -3.36px
  headline-lg:
    fontFamily: Esbuild
    fontSize: 80px
    fontWeight: 500
    lineHeight: 96px
    letterSpacing: -2.4px
  headline-md:
    fontFamily: Esbuild
    fontSize: 48px
    fontWeight: 600
    lineHeight: 56px
    letterSpacing: -1.2px
  headline-sm:
    fontFamily: Esbuild
    fontSize: 28px
    fontWeight: 400
    lineHeight: 28px
    letterSpacing: -0.56px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 22px
    letterSpacing: 0px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
    letterSpacing: -0.64px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    letterSpacing: 0px
  label-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 600
    lineHeight: 20px
    letterSpacing: 0px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 700
    lineHeight: 16px
    letterSpacing: 0px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 16px
    letterSpacing: 0px
  nav-link:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    letterSpacing: 0px
  micro:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 14px
    letterSpacing: 0px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  xl: 20px
  full: 9999px
spacing:
  xs: 6px
  sm: 14px
  md: 24px
  lg: 40px
  xl: 180px
components:
  button-primary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.tertiary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "14px 20px"
    height: "40px"
    width: "174px"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.tertiary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "14px 20px"
    height: "40px"
    width: "174px"
  button-link:
    backgroundColor: "transparent"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.none}"
    padding: "0px"
  card:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: "16px"
    height: "auto"
  input:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: "12px 14px"
    height: "40px"
  chip:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.micro}"
    rounded: "{rounded.full}"
    padding: "6px 10px"
---

# Huly Neon Dark

## Overview
Huly’s visual language feels futuristic, technical, and quietly playful, with a dark interface wrapped in electric blue and violet glow effects. It targets teams that want an all-in-one productivity platform with a premium, developer-friendly feel rather than a corporate SaaS aesthetic. The layout is spacious at the hero level but dense and information-rich in the app preview, balancing cinematic marketing with utilitarian product UI.

## Colors
- **Primary (#5683DA):** A cool electric blue used for links, active states, and subtle highlight accents; it carries the brand’s most recognizable tech-forward energy.
- **Primary Strong (#6C90F0):** A brighter blue variant that supports hover and glow moments without breaking the palette.
- **Secondary (#D1D1D1):** A soft neutral used for light button fills and lighter surface contrasts, especially where a muted control needs to stand out against black.
- **Tertiary (#5A250A):** A warm copper-brown used as button text and a grounding accent that contrasts the cool neon environment.
- **Neutral (#F6F6F6):** A pale off-white used for bright content and light cards when the brand needs readable contrast against dark surfaces.
- **Surface (#0B0C0F):** The dominant near-black canvas for the page background and top-level chrome.
- **Surface 2 (#17181B):** A slightly lifted dark gray used for cards, panels, and input-like regions inside the app preview.
- **On-surface (#FFFFFF):** Pure white for hero headlines, key button labels, and high-priority text.
- **On-surface-muted (#B8BCC6):** A softened cool gray for secondary copy, subdued nav items, and less prominent labels.
- **Border (#E5E7EB):** A light border tone used sparingly for definition in lighter UI contexts.
- **Border Strong (#FFFFFF1A):** A translucent border that keeps dark buttons and pills visible without feeling heavy.
- **Accent Glow (#7D5CFF):** A violet neon tone that appears in atmospheric beams and luminous gradients.
- **Accent Warm (#FF8A3D):** A hot orange glow used to energize CTA edges and add contrast to the blue lighting.
- **Error (#E85D5D):** A restrained red reserved for destructive or failure states.

## Typography
The system combines two distinct families: Esbuild for display headlines and Inter for interface text. Esbuild is used in large weights and tight tracking for the hero and section headlines, producing a compact, engineered look; the largest display styles feel bold, editorial, and almost condensed due to the strong negative letter spacing. Inter handles navigation, body copy, labels, and controls with a clean, highly readable rhythm.

Headlines should feel assertive and packed, with the heaviest styles reserved for hero messaging. Body text remains straightforward and low-drama, typically in 16px/24px or 18px/22px settings. Labels and buttons are compact at 12px, often bold, and designed to stay legible inside small pill-shaped controls. Uppercase styling is not dominant, but compact all-caps-like treatment can work for button labels when paired with strong weight and short copy.

## Layout
The layout uses a centered marketing composition with a very large visual hero and a wide, cinematic vertical emphasis running through the page. Space is generous around the primary headline and CTA, while the product screenshot below uses a denser, frame-like arrangement to showcase a complex interface. Spacing should follow the observed rhythm of 6px, 14px, 24px, 40px, and large hero separation around 180px when the design needs dramatic breathing room.

Primary content blocks should prefer wide containers with comfortable left/right margins rather than narrow editorial columns. Cards and panels inside the app preview use compact internal padding, but the overall page balances that density with substantial outer whitespace. Use section padding that increases sharply for hero or feature moments and decreases inside product chrome.

## Elevation & Depth
The page is mostly flat in the traditional sense, with very little reliance on shadows for hierarchy. Instead, depth comes from extreme color contrast, layered glows, luminous gradients, and subtle borders. The main product mockup appears to float because of halo-like edge lighting and bright energy spilling from behind it, not because of heavy drop shadow.

When cards and UI panels do use elevation, it is restrained: thin borders, soft tonal separation, and minimal shadowing. This keeps the interface feeling modern, sharp, and technologically precise rather than soft or neumorphic.

## Shapes
The shape language is rounded and pill-forward for actions, but otherwise compact and architectural. Buttons use full pill radii, while cards and panels typically settle into an 8px radius that keeps the product UI crisp. Overall, the system feels soft at the edges but disciplined in structure, avoiding excessive curvature except where it improves touch targets and CTA prominence.

## Components
Buttons are a defining brand element. `button-primary` should be the main CTA style: dark-filled or light-filled depending on context, pill-shaped, bold, and compact at about 40px tall with 14px/20px padding. It should feel tactile through border contrast and glow-adjacent lighting rather than through shadow. `button-secondary` is still a pill, but softer and more neutral, used for adjacent actions such as sign in or alternate pathways. `button-link` is minimal, text-only, and reserved for tertiary navigation or low-emphasis actions.

Cards should use the `card` token with a subtle border, dark surface, and 8px rounding. They should not introduce heavy shadows; use tonal layering and clear spacing instead. Inputs should match the same surface family as cards, with low-contrast borders and calm text colors so form elements feel integrated into the app rather than visually loud.

Chips and tags are small, rounded, and subdued, usually with muted text on dark surfaces. They work best when they support scannability inside dense panels, such as project lists, issue cards, and inbox items. Navigation elements are compact and low-contrast by default, then brighten or underline when active.

The hero CTA should remain short and high-contrast. Product chrome inside the app preview should stay information-dense, with tab-like controls, small icons, and tightly spaced lists that reinforce the platform’s utility-first character.

## Do's and Don'ts
- Do use deep near-black surfaces with bright white or blue text for the strongest brand recognition.
- Do keep primary actions pill-shaped and compact, with strong weight and minimal visual noise.
- Do rely on glow, contrast, and layering to create depth instead of heavy shadows.
- Do use Esbuild for large headlines and Inter for all interface copy, labels, and navigation.
- Don't introduce overly soft pastel palettes or friendly rounded cards that dilute the futuristic tone.
- Don't make buttons square or oversized; the rounded pill treatment is part of the brand.
- Don't overuse borders on dark surfaces; keep them subtle and intentional.
- Don't shift the UI into a light-first aesthetic unless it is a deliberate contrast panel or card.