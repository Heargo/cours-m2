import { TEXT } from "../lang/text.js";

export class AstrologyService {
  constructor(language = "en") {
    this.language = language;
    this.astrologicalSigns = TEXT[language].astrology.signs;
  }

  getAstrologyPrediction(sign) {
    if (this.astrologicalSigns.includes(sign)) {
      const allTemplates = TEXT[this.language].astrology.templates;

      //pick a random key
      const keys = Object.keys(allTemplates);
      const randomKey = keys[Math.floor(Math.random() * keys.length)];

      //pick a random template from the key
      const templates = allTemplates[randomKey];
      const template = templates[Math.floor(Math.random() * templates.length)];

      return this.fillTemplate(template);
    } else {
      return TEXT[this.language].astrology.invalid_sign;
    }
  }

  getRandomAstrologyPrediction() {
    const sign =
      this.astrologicalSigns[
        Math.floor(Math.random() * this.astrologicalSigns.length)
      ];
    return this.getAstrologyPrediction(sign);
  }

  fillTemplate(template) {
    // Generate funny variations
    const adjective = this.getRandomFunnyAdjective();
    const action = this.getRandomFunnyAction();
    const something = this.getRandomFunnySomething();

    return template
      .replace("{ADJECTIVE}", adjective)
      .replace("{INSERT AN ACTION}", action)
      .replace("{INSERT SOMETHING}", something);
  }

  getRandomFunnyAdjective() {
    const adjectives = TEXT[this.language].adjective;
    return adjectives[Math.floor(Math.random() * adjectives.length)];
  }

  getRandomFunnyAction() {
    const actions = TEXT[this.language].action;
    return actions[Math.floor(Math.random() * actions.length)];
  }

  getRandomFunnySomething() {
    const somethings = TEXT[this.language].something;
    return somethings[Math.floor(Math.random() * somethings.length)];
  }
}
