import type { CollectionEntry } from "astro:content"
import { DateTime } from "luxon"

export const defaultCampus = {
  darmstadt: "TU Darmstadt (Campus Stadtmitte)",
  frankfurt: "Goethe University Frankfurt (Campus Bockenheim)",
  mainz: "Johannes Gutenberg University Mainz",
}

export function printDate(date: Date) {
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "Europe/Berlin",
  })
}

export function printTime(date: Date) {
  return date.toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Europe/Berlin",
  })
}

function zeropad(n: number) {
  return n < 10 ? `0${n}` : `${n}`
}

/**
 * Convert a talk to an event for the add-to-calendar-button
 */
export function convertToATCB(talk: CollectionEntry<"talks">) {
  let name = `[DAIS] ${talk.data.speakerName}`
  if (talk.data.title) {
    name += ` - ${talk.data.title}`
  }
  let description = "Talk in the Discrete Algorithm Insights Seminar RMU[br]\n"
  description += "[url]https://dais.rhein-main-universitaeten.de[/url]"
  description += `[br][br]\n\nSpeaker: ${talk.data.speakerName}`
  if (talk.data.speakerAffiliation) {
    description += ` (${talk.data.speakerAffiliation})`
  }
  if (talk.data.title) {
    description += `[br]\nTitle: ${talk.data.title}`
  }
  if (talk.body) {
    description += `[br][br]\n\nAbstract: ${talk.body}`
  }
  const location = defaultCampus[talk.data.city]
  const datetime = DateTime.fromJSDate(talk.data.date, {
    zone: "Europe/Berlin",
  })
  const year = datetime.year
  const month = zeropad(datetime.month)
  const day = zeropad(datetime.day)
  const hour = zeropad(datetime.hour)
  const minute = zeropad(datetime.minute)
  const endTime = datetime.hour * 60 + datetime.minute + talk.data.duration
  const hourEnd = zeropad(Math.floor(endTime / 60))
  const minuteEnd = zeropad(endTime % 60)
  const e = {
    name,
    description,
    location,
    url: "https://dais.rhein-main-universitaeten.de/",
    startDate: `${year}-${month}-${day}`,
    startTime: `${hour}:${minute}`,
    endTime: `${hourEnd}:${minuteEnd}`,
    timeZone: "Europe/Berlin",
  }
  return e
}
