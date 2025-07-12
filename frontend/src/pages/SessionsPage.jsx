import useAuth from "@/hooks/useAuth";
import { get_array_index, get_param_url } from "@/utils/collections";
import { urls } from "@/utils/urls";
import { useState } from "react";
import { useEffect, useRef } from "react";
import { X } from "lucide-react";


import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import Spinner from "@/components/ui/Spinner";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { capitalize } from "@/utils/helpers";
import { toast } from "@/hooks/use-toast";
import SessionCard from "@/components/SessionCard";
import useSearchParams from "@/hooks/useSearchParams";

const MAX_PAGE_SIZE = 25;
const AVAILABLE_TYPES = ["all", "upcoming", "active", "old"]

const SessionPage = () => {
  const { auth_request } = useAuth();
  const { searchParams, setSearchParams } = useSearchParams();

  const [sessions, setSessions] = useState([]);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(2);
  const [fetchCounter, setFetchCounter] = useState(3);
  const [nextFetchUrl, setNextFetchUrl] = useState(get_param_url(urls.sessions.get_url(), { type: "all", size: size }));
  const [isFetching, setIsFetching] = useState(false);
  const fetching = useRef(isFetching);
  const [types, setTypes] = useState(["all"]);

  // Set types from search params
  useEffect(() => {
    console.log("Here")

    if (!searchParams.types) {
      return;
    }

    for (const t of searchParams.types) {
      update_types(t);
    }

  }, [])

  useEffect(() => {
    let no_change = true

    if (searchParams.types) {
      for (const type of types) {
        if (!searchParams.types.includes("type")) {
          no_change = false
          break;
        }
      }
    } else {
      no_change = false
    }

    if (no_change) {
      return;
    }

    setSearchParams(prev => {
      return {
        ...prev,
        types: types,
      }
    });

  }, [types])

  useEffect(() => {
    // Ignore if already fetching or no next page
    if (fetching.current || !nextFetchUrl || fetchCounter <= 0) {
      return;
    }

    fetch_sessions();

  }, [fetchCounter]);


  useEffect(() => {
    setPage(1);

  }, [types, size])

  const next_page = () => {
    const [si, ei] = get_array_index(page + 1, size)
    if (nextFetchUrl) {
      setFetchCounter(3);
    }

    if (psessions.length > si) {
      setPage(page + 1);
    }
  }

  const prev_page = () => {
    if (page <= 1) {
      return;
    }
    setPage(page - 1);
  }

  // Increase Fetch counter if current type of messages are not fully loaded
  useEffect(() => {
    if (fetchCounter > 0 || !nextFetchUrl) {
      return;
    }

    const [_, pg_ei] = get_array_index(page, size);

    if (get_sessions_for_types(types).length < pg_ei) {
      setFetchCounter(3);
    }
  });


  const fetch_sessions = async () => {

    update_isFetching(true);
    const { json, error } = await auth_request(
      nextFetchUrl,
      {
        method: "GET"
      }
    );
    update_isFetching(false);

    if (error) {
      console.warn("failed to fetch sessions ");
      return;
    }

    setNextFetchUrl(json.next_url)
    setSessions(sessions => [...sessions, ...json.items]);
    setFetchCounter(prev => prev - 1);
  }

  const update_types = (value) => {
    if (!AVAILABLE_TYPES.includes(value)) {
      return;
    }

    setTypes(prev => {
      if (prev.includes(value)) {
        return prev
      }

      if (value == "all") {
        return ["all"]
      }

      const _types = [...prev]
      const all_i = _types.findIndex(v => v == "all")
      if (all_i != -1) {
        _types.splice(all_i, 1);
      }
      return [..._types, value]
    })


  }

  const update_isFetching = (val = false) => {
    if (isFetching != val) {
      setIsFetching(val);
    }
    fetching.current = val
  }

  const get_sessions_for_types = (types) => {
    if (types.includes("all")) {
      return sessions;
    }
    return sessions.filter(session => types.includes(session.type));
  }

  const psessions = get_sessions_for_types(types)
  const [si, ei] = get_array_index(page, size);


  return (
    <div className="dark:text-white m-2 gap-5 flex flex-col">
      <div className="flex justify-between">

        <div
          className={cn(
            "inline-flex items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground",
            "w-min gap-2"
          )}
        >
          <div className={cn(
            "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow",
            "bg-black text-foreground h-full"
          )}>
            <Select
              onValueChange={update_types}
              value=""
            // defaultValue="something"
            >
              <SelectTrigger className="w-[180px] border-0">
                <SelectValue placeholder="Select Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Types</SelectLabel>
                  <SelectItem value="all">All</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="upcoming">Upcoming</SelectItem>
                  <SelectItem value="old">Old</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <div className={cn(
            "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow",
            "bg-black text-foreground h-full",
            "px-3"
          )}>
            <div className="flex justify-center items-center gap-2">
              Page Size
              <Input type="number" className="min-w-32 border-0" onChange={e => setSize(parseInt(e.target.value), 10)} value={size} min={1} max={MAX_PAGE_SIZE} />
            </div>
          </div>
        </div>

        <div className="flex items-center w-fit h-full ">
          <div className="flex gap-2 h-full items-center">
            {
              types.map(type => {
                return (
                  <div className="relative" key={type}>
                    <Badge variant="secondary" className="w-16 h-8 flex justify-center ">
                      {capitalize(type)}
                    </Badge>
                    <X data-type={type} className="absolute right-1 top-1" size={12}
                      onClick={(e) => {
                        console.log(e);
                        const index = types.findIndex((val) => val == e.target.dataset.type);
                        if (index == -1) {
                          return;
                        }
                        if (types.length == 1) {
                          toast({
                            description: "Atleast one type filter is required",
                            variant: "destructive"
                          });
                          return;
                        }
                        setTypes(types => {
                          const _types = [...types]
                          _types.splice(index, 1);
                          return _types
                        });
                      }}

                    />
                  </div>
                )
              })
            }
          </div>
        </div>

      </div>

      <div className="flex flex-col items-center" >
        {psessions.slice(si, ei).map(session => {
          return (
            <SessionCard session={session} key={session.id} />
          )
        })}
      </div>

      <div>
        <Pagination
          className="justify-end"
        >
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                to={"#"}
                onClick={(e) => {
                  e.preventDefault();
                  if (fetching.current) {
                    return;
                  }
                  prev_page();
                }}
                className="dark:text-white hover:dark:bg-gray-700"
              />
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                isActive={true}
                to={"/sessions"}
                className="dark:text-white dark:border dark:border-gray-400 hover:dark:bg-gray-700"
              >
                {
                  fetching.current ?
                    <Spinner spinning={isFetching} />
                    : page
                }
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationNext to={"#"}
                onClick={(e) => {
                  e.preventDefault();
                  if (fetching.current) {
                    return;
                  }
                  next_page();
                }}
                className="dark:text-white hover:dark:bg-gray-700"
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  )
}

export default SessionPage
