const { add, subtract } = require("./arithmetic");

describe("Arithmetic Functions", () => {
  // Test addition
  test("Addition", () => {
    const result = add(5, 3);
    expect(result).toBe(8);
  });

  // Test subtraction
  test("Subtraction", () => {
    const result = subtract(5, 3);
    expect(result).toBe(2);
  });
});
