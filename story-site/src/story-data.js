/** @typedef {{ id: string, number: string, ingredientNumber?: string, title: string, emphasis: string, kicker: string, body: string, frame: string, sequenceFrame: number, ingredient?: string }} StoryChapter */

/** @type {StoryChapter[]} */
export const chapters = [
  { id: 'kitchen', number: '01', title: 'A little', emphasis: 'alchemy.', kicker: 'The kitchen', body: 'A quiet pause before the first ingredient arrives. Warm light, cool glass, and a counter ready for something fresh.', frame: 'kitchen', sequenceFrame: 0 },
  { id: 'lemon', number: '02', ingredientNumber: '01', title: 'A bright', emphasis: 'first note.', kicker: '01 / Lemon', ingredient: 'Lemon', body: 'A flash of citrus sets the whole story in motion.', frame: 'lemon', sequenceFrame: 4 },
  { id: 'lime', number: '03', ingredientNumber: '02', title: 'A lively', emphasis: 'edge.', kicker: '02 / Lime', ingredient: 'Lime', body: 'A sharper green note joins the swirl.', frame: 'lime', sequenceFrame: 7 },
  { id: 'apple', number: '04', ingredientNumber: '03', title: 'Crisp,', emphasis: 'gently sweet.', kicker: '03 / Apple', ingredient: 'Apple', body: 'Cool, crisp apple rounds out the citrus.', frame: 'apple', sequenceFrame: 10 },
  { id: 'aloe', number: '05', ingredientNumber: '04', title: 'Cool,', emphasis: 'clean green.', kicker: '04 / Aloe vera', ingredient: 'Aloe vera', body: 'A whole aloe leaf brings a sculptural, unmistakably fresh beat.', frame: 'aloe', sequenceFrame: 13 },
  { id: 'kiwi', number: '06', ingredientNumber: '05', title: 'A little', emphasis: 'tang.', kicker: '05 / Kiwi', ingredient: 'Kiwi', body: 'A bright botanical note, vivid at the centre.', frame: 'kiwi', sequenceFrame: 16 },
  { id: 'dandelion', number: '07', ingredientNumber: '06', title: 'Wild,', emphasis: 'in a good way.', kicker: '06 / Dandelion', ingredient: 'Dandelion', body: 'A whole above-ground dandelion plant drifts into frame: flower, stems, and leaves. No roots.', frame: 'dandelion', sequenceFrame: 19 },
  { id: 'okra', number: '08', ingredientNumber: '07', title: 'A soft', emphasis: 'finish.', kicker: '07 / Okra', ingredient: 'Okra', body: 'The final green ingredient completes the line-up.', frame: 'okra', sequenceFrame: 22 },
  { id: 'whirl', number: '09', title: 'Seven good things,', emphasis: 'finding rhythm.', kicker: 'The gathering', body: 'The ingredients lift together, circling into a vivid, kinetic spiral.', frame: 'whirl', sequenceFrame: 26 },
  { id: 'blend', number: '10', title: 'Fresh,', emphasis: 'blended.', kicker: 'The blend', body: 'The swirl resolves into a smooth green pour, caught in the light.', frame: 'blend', sequenceFrame: 32 },
  { id: 'pour', number: '11', title: 'Made for', emphasis: 'the moment.', kicker: 'The final pour', body: 'A chilled bottle waits at the end of the journey. The last frame, and a fresh beginning.', frame: 'pour', sequenceFrame: 44 },
];

export const SEQUENCE_FRAME_COUNT = 45;

/** Scroll progress for the cinematic stage, kept pure for easy testing. */
export function getProgress(index, total) {
  if (!Number.isFinite(total) || total <= 1) return 0;
  return Math.min(100, Math.max(0, Math.round((index / (total - 1)) * 100)));
}

export function getAnimaticImageName(index, frame) {
  const assetFrame = frame === 'aloe' ? 'aloe-vera' : frame;
  return `${String(index).padStart(2, '0')}-${assetFrame}.webp`;
}
