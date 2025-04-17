
import { createContext, useContext } from "react";
import useAuth from "@/hooks/useAuth";
import  {urls} from "@/utils/urls"
import { useEffect, useState } from "react";
import { get_param_url } from "@/utils/collections";
import { toast } from "@/hooks/use-toast";

const WalletContext = createContext({
  wallet: null,
  recharges: [],
});

const WalletContextProvider = ({children}) => {
  const {logged, auth_request} = useAuth();

  const [wallet, setWallet] = useState(null);
  const [recharges, setRecharges] = useState([]);


  useEffect(() => {
    if (!logged){
      return;
    }

    // Fetch Wallet
    fetch_wallet();

  }, [logged])

  const fetch_wallet = async () => {
    const {json, error} = await auth_request(
      urls.wallet.get_url(),
      {
        method: "GET",
      }
    )

    if (error){
      toast({
        description: "Failed to fetch wallet",
        variant: "destructive"
      })
      return
    }

    setWallet(json);
  }

  const fetch_recharge = async (page, size) => {
    return await auth_request(
      get_param_url(urls.recharges.get_url(), {page, size}),
      {
        method: "GET"
      }
    )
  }

  return <WalletContext.Provider
  value={{
    wallet,
    fetch_wallet,
    recharges,
    fetch_recharge,
    setRecharges,
  }}
  >
    {children}
  </WalletContext.Provider>
}

export {
  WalletContext,
  WalletContextProvider,
}
