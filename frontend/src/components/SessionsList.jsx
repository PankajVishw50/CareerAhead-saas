
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
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import Spinner from "@/components/ui/Spinner";
import SessionCard from "@/components/SessionCard";
import { get_array_index } from "@/utils/collections";
import { AlertCircleIcon } from "lucide-react"

const SessionsList = ({ sessions, pagination = true, page = 0, size = 10, next_page, prev_page, fetching = false }) => {
  let [si, ei] = get_array_index(page, size);
  const fsessions = pagination ? sessions.slice(si, ei) : sessions

  return (
    <div>
      {
        sessions.length > 0 ? (
          <div className="flex flex-col items-center" >
            {fsessions.map(session => {
              return (
                <SessionCard session={session} key={session.id} />
              )
            })}
          </div>
        ) : (
          <div className="w-full justify-self-center flex gap-2 justify-center items-center p-5 border-red-500 text-red-500">
            <AlertCircleIcon size={18} /> No Session Found
          </div>
        )

      }


      {
        pagination && (
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
                      if (fetching) {
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
                      fetching ?
                        <Spinner spinning={fetching} />
                        : page
                    }
                  </PaginationLink>
                </PaginationItem>
                <PaginationItem>
                  <PaginationNext to={"#"}
                    onClick={(e) => {
                      e.preventDefault();
                      if (fetching) {
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
        )
      }

    </div>
  )
}

export default SessionsList
