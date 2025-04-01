
const get_array_index = (page, size) => {
  return [
    (page-1)*size,
    page * size
  ]
}

export {
  get_array_index,
}