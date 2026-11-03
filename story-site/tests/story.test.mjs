import test from 'node:test';
import assert from 'node:assert/strict';
import { access } from 'node:fs/promises';
import { chapters, getAnimaticImageName, getProgress, SEQUENCE_FRAME_COUNT } from '../src/story-data.js';

test('story has a single ordered journey from kitchen to final pour', () => {
  assert.equal(chapters[0].id, 'kitchen');
  assert.equal(chapters.at(-1).id, 'pour');
  assert.equal(chapters.length, 11);
  assert.equal(new Set(chapters.map(({ id }) => id)).size, chapters.length);
});

test('scroll keyframes follow the Blender timeline and stay ordered', () => {
  const sequenceFrames = chapters.map(({ sequenceFrame }) => sequenceFrame);
  assert.deepEqual(sequenceFrames, [0, 4, 7, 10, 13, 16, 19, 22, 26, 32, 44]);
  assert.ok(sequenceFrames.every((frame, index) => frame >= 0 && frame < SEQUENCE_FRAME_COUNT && (index === 0 || frame > sequenceFrames[index - 1])));
});

test('ingredient chapters match the agreed seven ingredients and order', () => {
  const ingredients = chapters.filter(({ ingredient }) => ingredient);
  assert.deepEqual(ingredients.map(({ ingredient }) => ingredient), ['Lemon', 'Lime', 'Apple', 'Aloe vera', 'Kiwi', 'Dandelion', 'Okra']);
  assert.deepEqual(ingredients.map(({ ingredientNumber }) => ingredientNumber), ['01', '02', '03', '04', '05', '06', '07']);
  assert.match(chapters.find(({ id }) => id === 'dandelion').body, /No roots/);
});

test('progress stays within bounds and handles a single chapter', () => {
  assert.equal(getProgress(0, 11), 0);
  assert.equal(getProgress(5, 11), 50);
  assert.equal(getProgress(10, 11), 100);
  assert.equal(getProgress(0, 1), 0);
  assert.equal(getProgress(-1, 11), 0);
});

test('each story chapter has a corresponding Blender frame asset', async () => {
  await Promise.all(chapters.map((chapter, index) => access(new URL(`../assets/animatic/${getAnimaticImageName(index, chapter.frame)}`, import.meta.url))));
});

test('the scroll sequence contains every numbered frame', async () => {
  assert.equal(SEQUENCE_FRAME_COUNT, 45);
  await Promise.all(Array.from({ length: SEQUENCE_FRAME_COUNT }, (_, index) =>
    access(new URL(`../assets/sequence/frame-${String(index).padStart(3, '0')}.webp`, import.meta.url))));
});
