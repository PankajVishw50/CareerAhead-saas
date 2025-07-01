
const abs_url = (url_path) => {
  return import.meta.env.VITE_API_URL + url_path
}



const urls = {
  user: {
    get_url: () => urls.user.url,
    url: "/api/auth/me"
  },
  login: {
    url: "/api/auth/login",
    get_url: () => urls.login.url,
  },
  logout: {
    url: "/api/auth/logout",
    get_url: () => urls.logout.url,
  },
  access_token: {
    url: "/api/auth/token/access",
    get_url: () => urls.access_token.url,
  },
  signed_token: {
    url: "/api/auth/token/signed-token",
    get_url: () => urls.signed_token.url,
  },
  ws_notification: {
    url: "/ws/notification",
    get_url: () => urls.ws_notification.url,
  },
  counsellors: {
    url: "/api/counsellors",
    get_url: () => urls.counsellors.url,
  },
  counsellor: {
    url: "/api/counsellors/:counsellor_id",
    get_url: (id) => urls.counsellor.url.replace(":counsellor_id", id),
  },
  available_slots: {
    url: "/api/counsellors/:counsellor_id/slots/available",
    get_url: (counsellor_id) => urls.available_slots.url.replace(":counsellor_id", counsellor_id),
  },
  recharges: {
    url: "/api/wallet/recharges",
    get_url: () => urls.recharges.url,
  },
  verify_recharge: {
    url: "/api/wallet/recharges/:recharge_id/verify",
    get_url: (recharge_id) => urls.verify_recharge.url.replace(":recharge_id", recharge_id),
  },
  wallet: {
    url: "/api/wallet",
    get_url: () => urls.wallet.url
  },
  counsellor_sessions: {
    url: "/api/counsellors/:counsellor_id/slots/:slot_id/sessions",
    get_url: (counsellor_id, slot_id) => urls.counsellor_sessions.url.replace(":counsellor_id", counsellor_id).replace(":slot_id", slot_id),
  },
  sessions: {
    url: "/api/counsellors/sessions",
    get_url: () => urls.sessions.url,
  },
  messages: {
    url: "/api/chats/:chat_id/messages",
    get_url: (chat_id) => urls.messages.url.replace(":chat_id", chat_id),
  },
  chat: {
    url: "/api/chats/:chat_id",
    get_url: (chat_id) => urls.chat.url.replace(":chat_id", chat_id),
  },
  chats: {
    url: "/api/chats",
    get_url: () => urls.chats.url,
  },
}

export {
  urls,
}
