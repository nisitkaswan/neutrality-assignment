import { test, expect } from '@playwright/test';


test.describe('UserList Component Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000', { timeout: 30000 });
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-test-id="fetch-users-button"]', { state: 'visible', timeout: 10000 });
  });

  test('initial render', async ({ page }) => {
    const fetchButton = page.locator('[data-test-id="fetch-users-button"]');
    await expect(fetchButton).toBeVisible({ timeout: 10000 });

    const currentUsersList = page.locator('[data-test-id="current-users-list"]');
    const allUsersList = page.locator('[data-test-id="all-users-list"]');

    await expect(currentUsersList).toBeVisible({ timeout: 10000 });
    await expect(allUsersList).toBeVisible({ timeout: 10000 });
  });

  test('fetching users', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    await page.click('[data-test-id="fetch-users-button"]');

    await page.waitForLoadState('networkidle');

    await page.waitForSelector('[data-test-id^="all-user-"]', { state: 'visible', timeout: 10000 });

    const newUserCount = await page.locator('[data-test-id^="all-user-"]').count();
    expect(newUserCount).toBeGreaterThan(5);
  });


});