
const get_datetime = () => {
  return new Date()
}

const datetime_formatted = (date=null) => {
  date = date ?? get_datetime()

  const pad = (num) => num.toString().padStart(2, '0');

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}

const datetime_formatted_tz = (date=null) =>  {
    date = date ?? get_datetime()

    const datetime_str = datetime_formatted(date);
    const pad = (num) => num.toString().padStart(2, '0');

    // Get timezone offset in minutes
    let tzOffset = date.getTimezoneOffset();
    const tzSign = tzOffset <= 0 ? '+' : '-';
    tzOffset = Math.abs(tzOffset);
    const tzHours = pad(Math.floor(tzOffset / 60));
    const tzMinutes = pad(tzOffset % 60);

    return `${datetime_str}${tzSign}${tzHours}${tzMinutes}`;
}

const date_formatted = (date=null) => {
    date = date ?? get_datetime()

    return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
}

const timezone_formatted = () => {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
}

const get_datetime_end = (date=null) => {
    date = date ?? get_datetime()

    date.setHours(23)
    date.setMinutes(59)
    date.setSeconds(59)
    date.setMilliseconds(999)

    return date
}


const time_formatted = (date=null) => {
    date = date ?? get_datetime()

    let hours = date.getHours();
    let minutes = date.getMinutes();

    // Determine AM or PM mode
    const mode = hours >= 12 ? 'PM' : 'AM';

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')} ${mode}`;
}

export {
    get_datetime,
    datetime_formatted,
    datetime_formatted_tz,
    date_formatted,
    timezone_formatted,
    get_datetime_end,
    time_formatted,
}
