import { Separator } from "@/components/ui/separator";
import useAuth from "@/hooks/useAuth";
import { cn } from "@/lib/utils";
import { urls } from "@/utils/urls";
import { useEffect, useState } from "react";
import { DribbbleIcon, TwitchIcon, TwitterIcon } from "lucide-react";
import { Link } from "react-router"
import { Button } from "@/components/ui/button"
import { toast } from "@/hooks/use-toast";
import { get_array_index, get_param_url, paise_to_rupees } from "@/utils/collections";
import SessionsList from "@/components/SessionsList";
import { useParams } from "react-router";
import UserProfile from "@/components/UserProfile"
import CounsellorProfile from "@/components/CounsellorProfile";
import useSearchParams from "@/hooks/useSearchParams";
import ProfileCardSkeleton from "@/components/ProfileCardSkeleton";
import { Skeleton } from "@/components/ui/skeleton";

const InteractionPage = ({ }) => {
  const { auth_request, user: auth_user } = useAuth();
  const { counsellor_id, user_id } = useParams();
  const { searchParams } = useSearchParams();

  const [counsellor, setCounsellor] = useState();
  const [user, setUser] = useState();
  const [stats, setStats] = useState();
  const [sessions, setSessions] = useState([]);
  const [nextSessionUrl, setNextSessionUrl] = useState(get_param_url(urls.sessions.get_url(), { user: user_id, counsellor: counsellor_id }))
  const [retries, setRetries] = useState(3);
  const [view,] = useState(() => {
    if (!searchParams.view || !["counsellor", "user"].includes(searchParams.view[0])) {
      return "user"
    }
    return searchParams.view[0]
  });

  const [page, setPage] = useState(1);
  const [size,] = useState(10);

  let profileCard = null;
  switch (view) {
    case (counsellor && "user"):
      profileCard = <CounsellorProfile counsellor={counsellor} />;
      break;
    case (user && "counsellor"):
      profileCard = <UserProfile user={user} />;
      break;
    default:
      profileCard = <ProfileCardSkeleton />;

  }

  // Fetch User
  useEffect(() => {
    // Check if user is authenticated user.
    if (auth_user && auth_user.id === user_id) {
      setUser(auth_user);
    }

    (async () => {
      const { json, error } = await auth_request(
        urls.user.get_url(user_id),
      )

      if (error) {
        console.error(error)
        return toast({
          description: "Failed to fetch user data",
          variant: "destructive",
        });
      }

      setUser(json);
    })()
  }, [])

  // Fetch Counsellor
  useEffect(() => {
    (async () => {
      const { json, error } = await auth_request(
        urls.counsellor.get_url(counsellor_id),
      )

      if (error) {
        console.error(error)
        return toast({
          description: "Failed to fetch counsellor data",
          variant: "destructive",
        });
      }

      setCounsellor(json);
    })()
  }, [])

  // Fetch Counsellor-User Stats
  useEffect(() => {
    (async () => {
      const { json, error } = await auth_request(
        get_param_url(urls.counsellor_stats.get_url(counsellor_id), { user_id: user_id }),
      )

      if (error) {
        console.error(error)
        return toast({
          description: "Failed to fetch stats",
          variant: "destructive",
        });
      }

      setStats(json);
    })()
  }, [])

  // Fetch Sessions
  useEffect(() => {
    if (!nextSessionUrl || retries <= 0) {
      return;
    }

    (async () => {
      const { json, error } = await auth_request(
        nextSessionUrl,
      )

      if (error) {
        setRetries(prev => prev - 1)
        console.error(error)
        return toast({
          description: "Failed to fetch sessions",
          variant: "destructive",
        });
      }

      setSessions(prev => {
        return [...prev, ...json.items.filter(item => !prev.find(p => p.id === item.id))]
      });
      setRetries(3);
      setNextSessionUrl(json.next_url)
    })()
  }, [nextSessionUrl, retries])

  const next_page = () => {
    const [si, ei] = get_array_index(page + 1, size)

    if (sessions.length > si) {
      setPage(page + 1);
    }
  }

  const prev_page = () => {
    if (page <= 1) {
      return;
    }
    setPage(page - 1);
  }



  return (
    <div className="dark:text-white flex flex-col gap-4 max-w-5xl justify-self-center place-self-center w-full">
      <div className="flex gap-10 flex-col lg:flex-row lg:justify-center justify-center items-center">
        {profileCard}

        <div className="grid grid-cols-3 grid-rows-2 gap-x-10 gap-y-16 justify-center justify-items-baseline">
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl md:text-2xl font-bold text-indigo-500">
              {stats ? stats.user_interaction.total_sessions + "+" : <Skeleton className="h-5 w-20 rounded bg-indigo-500/10" />}
            </span>
            <p className="mt-6 font-semibold text-md text-center">
              Total Sessions
            </p>
          </div>
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl md:text-2xl font-bold text-indigo-500">
              {stats ? paise_to_rupees(stats.user_interaction.total_earnings) + " RS" : <Skeleton className="h-5 w-20 rounded bg-indigo-500/10" />}
            </span>
            <p className="mt-6 font-semibold text-md text-center">
              Transactions
            </p>
          </div>
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl md:text-2xl font-bold text-[#A3DC9A]">
              {stats ? stats.user_interaction.active_sessions + "+" : <Skeleton className="h-5 w-20 rounded bg-[#A3DC9A]/10" />}
            </span>
            <p className="mt-6 font-semibold text-md text-center">
              Active Sessions
            </p>
          </div>
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl md:text-2xl font-bold text-indigo-500">
              {stats ? stats.user_interaction.upcoming_sessions + "+" : <Skeleton className="h-5 w-20 rounded bg-indigo-500/10" />}
            </span>
            <p className="mt-6 font-semibold text-md text-center">
              Upcoming Sessions
            </p>
          </div>
          <div className="flex flex-col justify-center items-center">
            <span className="text-xl md:text-2xl font-bold text-[#FF894F]">
              {stats ? stats.user_interaction.old_sessions + "+" : <Skeleton className="h-5 w-20 rounded bg-[#FF894F]/10" />}
            </span>
            <p className="mt-6 font-semibold text-md text-center">
              Old Sessions
            </p>
          </div>
        </div>
      </div>

      <div>
        <h1 className="text-xl my-2">Active Sessions</h1>
        {/* <SessionsList sessions={sessions.filter(session => session.type === "active")} pagination={false} /> */}
        <SessionsList sessions={sessions.filter(session => session.type === "fjelfjek")} pagination={false} />
      </div>

      <div>
        <h1 className="text-xl my-2">All Sessions</h1>
        <SessionsList sessions={sessions} page={page} size={size} next_page={next_page} prev_page={prev_page} />
      </div>

    </div >
  )
}

export default InteractionPage
