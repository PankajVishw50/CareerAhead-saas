import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { useEffect, useState } from "react";
import {useOutletContext} from "react-router";
import {Plus, Minus} from "lucide-react";
import useAuth from "@/hooks/useAuth";
import { urls } from "@/utils/urls";
import Spinner from "@/components/ui/Spinner";
import RechargeHistory from "@/components/RechargeHistory";
import useWallet from "@/hooks/useWallet";
import { toast } from "@/hooks/use-toast";

const WalletPage = () => {
  const {setHeaderTitle} = useOutletContext();
  const {auth_request} = useAuth();
  const {setRecharges, fetch_wallet} = useWallet();


  const MIN_RVAL = 100;
  const MAX_RVAL = 9999;
  const [rechargeValue, setRechargeValue] = useState(MIN_RVAL);
  const [rechargeInProgress, setRechargeInProgress] = useState(false);

  const handle_recharge_value_change = (v) => {

    const nv = rechargeValue + v
    setRechargeValue(nv);
  }

  useEffect(() => {
    setHeaderTitle("Wallet");

    return (() => {
      setHeaderTitle("")
    })
  }, [])

  const handle_recharge_form_submit = async (e) => {
    e.preventDefault();

    // Convert Rs to paise
    const paise = rechargeValue * 100;
    setRechargeInProgress(true);
    const {response, json, error} = await auth_request(
      urls.recharges.get_url(),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "amount": paise
        }),
      }
    )

    if (error){
      setRechargeInProgress(false);
      toast({
        description: "Recharge Failed",
        variant: "destructive"
      });
      return
    }
    setRecharges([]);

    // Open Razorpay
    openRazorpay(
      json,
      async (response) => {
        // 🔁 Send response.razorpay_payment_id and order ID to backend

        // Verify Recharge
        const {json2, error} = await auth_request(
          urls.verify_recharge.get_url(json.id),
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              payment_id: response.razorpay_payment_id,
              signature: response.razorpay_signature,
            })
          }
        )
        setRechargeInProgress(false);

        if (error){
          toast({
            description: "Failed to verify recharge, any valid amount will be refunded",
            variant: "destructive"
          });
          return;
        }

        toast({
          description: "Recharge Successfull",
        });
        fetch_wallet();
      },
      () => {
        setRechargeInProgress(false);
      }
    )

  }

  const openRazorpay = (orderData, handler, modal_clossed_handler) => {
    const options = {
      key: import.meta.env.VITE_RAZORPAY_API_KEY, // 🔐 Replace with your Razorpay Key ID
      amount: orderData.amount, // amount in paise
      currency: orderData.currency,
      name: "CareerAhead Corp.",
      description: "Wallet Top-Up",
      order_id: orderData.order_id, // Order ID from backend
      handler: handler,
      prefill: {
        name: "Pankaj", // optional
        email: "pankaj@example.com", // optional
      },
      theme: {
        color: "#22c55e", // Tailwind green-500
      },
      modal: {
        ondismiss: modal_clossed_handler,
      },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  }

  return (
    <div className="dark:text-white flex gap-2 flex-col my-2">
      <div className="border w-full flex flex-col gap-4 justify-center items-center py-10">
        <form className="flex gap-5 flex-col"
        onSubmit={handle_recharge_form_submit}
        >
          <div className="flex gap-3">
            <Button
            type="button"
            onClick={() => handle_recharge_value_change(-50)}
            ><Minus/></Button>
            <div>
              <Input type="number"
              className="no-input-sidebar w-[100px]"
              min={MIN_RVAL}
              max={MAX_RVAL}
              required={true}
              onChange={(e) => {
                setRechargeValue(e.target.value);
              }}
              value={rechargeValue}
              />
            </div>
            <Button
            type="button"
            onClick={() => handle_recharge_value_change(50)}
            ><Plus/></Button>
          </div>
          <div>
            <Button className="w-full" type="submit"
            disabled={rechargeInProgress}>
              {
                rechargeInProgress ? (
                  <Spinner spinning={true} className="text-black"/>
                )
                : "Recharge"
              }
              </Button>
          </div>
        </form>
      </div>
      <Separator/>

      <RechargeHistory/>
    </div>
  )
}

export default WalletPage;
