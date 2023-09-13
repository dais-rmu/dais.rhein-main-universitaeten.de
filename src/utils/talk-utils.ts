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
