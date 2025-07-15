const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

const get_name_initials = (name, max_chars = 3) => {
  const names = name.split(" ");
  let initial = "";
  for (const name of names.slice(0, max_chars)) {
    initial += name.trim()[0].toUpperCase()
  }
  return initial
}

export {
  capitalize,
  get_name_initials,
}

