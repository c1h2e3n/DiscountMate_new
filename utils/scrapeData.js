const puppeteer = require("puppeteer");
const cheerio = require("cheerio");

const scrapeDataItem = ($, selector) => {
  const text = $(selector).text().trim();
  return text ? text : "";
};

const scrapeData = async (url, page) => {
  try {
    await page.goto(url, { waitUntil: "load", timeout: 0 });
    const html = await page.evaluate(() => document.body.innerHTML);
    const $ = await cheerio.load(html);

    let title = scrapeDataItem(
      $,
      "#coles-targeting-main-container > div > div.sc-3cdb92df-9.hLNHTa.coles-targeting-StylesProductDetailStylesProductCTAWrapper > div.sc-b104d029-0.fvqxHq.coles-targeting-ProductBuyProductBuyContainer > h1"
    );

    let price = scrapeDataItem(
      $,
      "#coles-targeting-main-container > div > div.sc-3cdb92df-9.hLNHTa.coles-targeting-StylesProductDetailStylesProductCTAWrapper > div.sc-9a1967ae-0.dibXQr.coles-targeting-ProductBuyProductBuyContainer > section > div.price > span.price__value"
    );

    let discount = scrapeDataItem(
      $,
      "#coles-targeting-main-container > div > div.sc-3cdb92df-9.hLNHTa.coles-targeting-StylesProductDetailStylesProductCTAWrapper > div.sc-9a1967ae-0.dibXQr.coles-targeting-ProductBuyProductBuyContainer > section > div.price > span.sc-24d55302-0.hISgRS.badge.is-small.badge.is-small"
    );

    let productDetails = scrapeDataItem(
      $,
      "#coles-targeting-main-container > div > div.sc-3cdb92df-10.kQMQza.coles-targeting-StylesProductDetailStylesProductDetailsWrapper > div.sc-4371e03a-0.kSMoWS.coles-targeting-ProductDetailsContainer > div.sc-f639a49e-0.ilwNff.product-details.product-details > div > div > div"
    );

    let imgUrl = $(
      "#coles-targeting-main-container > div > div.sc-3cdb92df-4.evQUZs > div > div > div > div.sc-d0071c16-2.iJzwco.coles-targeting-HeroCarouselHeroCarouselControlsWrapper > div > div > div > ul > li:nth-child(1) > button > div > img"
    ).attr("src");

    return {
      title,
      price,
      discount,
      productDetails,
      imgUrl,
    };
  } catch (error) {
    console.log(error);
  }
};

module.exports = scrapeData;
