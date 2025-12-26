import { z, defineCollection } from "astro:content"
import { DateTime } from "luxon"

const talksCollection = defineCollection({
  type: "content",
  schema: z.object({
    speakerName: z.string(),
    speakerAffiliation: z.string().optional(),
    speakerURL: z.string().url().optional(),
    title: z.string().optional(),
    date: z
      .string()
      .regex(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/)
      .transform((s) =>
        DateTime.fromSQL(s, { zone: "Europe/Berlin" }).toJSDate(),
      ),
    duration: z.number().default(60),
    city: z.enum(["darmstadt", "frankfurt", "mainz"]),
    campus: z.string().optional(),
    room: z.string().optional(),
    mapURL: z.string().url().optional(),
  }),
})

export const collections = {
  talks: talksCollection,
}
