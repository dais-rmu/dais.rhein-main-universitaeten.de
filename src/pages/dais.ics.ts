import { createEvents, type EventAttributes } from "ics"
import { getCollection } from "astro:content"
import { defaultCampus } from "../utils/talk-utils"
import { DateTime } from "luxon"
import { date } from "astro/zod"

const allTalks = (await getCollection("talks")).toSorted(
  (t1, t2) => t1.data.date.valueOf() - t2.data.date.valueOf(),
)

function convertToICS(talk: (typeof allTalks)[0]): EventAttributes {
  let title = `[DAIS] ${talk.data.speakerName}`
  if (talk.data.title) {
    title += ` - ${talk.data.title}`
  }
  let description = `Speaker: ${talk.data.speakerName}`
  if (talk.data.speakerAffiliation) {
    description += ` (${talk.data.speakerAffiliation})`
  }
  if (talk.data.title) {
    description += `\nTitle: ${talk.data.title}`
  }
  if (talk.body) {
    description += `\n\nAbstract: ${talk.body}`
  }
  const location = defaultCampus[talk.data.city]
  const datetime = DateTime.fromJSDate(talk.data.date)
  const year = datetime.year
  const month = datetime.month
  const day = datetime.day
  const hour = datetime.hour
  const minute = datetime.minute
  console.log(hour)
  const e: EventAttributes = {
    title,
    description,
    location,
    url: "https://dais.rhein-main-universitaeten.de/",
    start: [year, month, day, hour, minute],
    duration: { minutes: 60 },
  }
  return e
}

const { error, value } = createEvents(allTalks.map(convertToICS))

if (error) {
  console.error(error)
}
// export const GET = () => {
//   return new Response(value, {
//     status: 200,
//     headers: {
//       "Content-Type": "text/calendar",
//     },
//   })
// }
