import { TEXT } from "../lang/text.js";

export class CustomFortuneService {
  constructor(language = "en") {
    this.language = language;
    this.categories = TEXT[language].fortune.categories;
  }

  getCustomFortune(category) {
    if (this.categories.includes(category)) {
      const predictionTemplates = TEXT[this.language].fortune.templates;

      return this.fillTemplate(predictionTemplates, category);
    } else {
      return TEXT[this.language].fortune.invalid_category;
    }
  }

  getRandomCustomFortune() {
    const category =
      this.categories[Math.floor(Math.random() * this.categories.length)];
    return this.getCustomFortune(category);
  }

  fillTemplate(templates, category) {
    const template = templates[Math.floor(Math.random() * templates.length)];

    // Generate funny variations
    const adjective = this.getRandomFunnyAdjective();
    const something = this.getRandomFunnySomething();

    return template
      .replace("{CATEGORY}", category)
      .replace("{ADJECTIVE}", adjective)
      .replace("{INSERT SOMETHING}", something);
  }

  getRandomFunnyAdjective() {
    const adjectives = TEXT[this.language].adjective;
    return adjectives[Math.floor(Math.random() * adjectives.length)];
  }

  getRandomFunnySomething() {
    const somethings = TEXT[this.language].something;
    return somethings[Math.floor(Math.random() * somethings.length)];
  }
}
