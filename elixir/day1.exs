# New year's resolution: get better at Elixir

defmodule Day1 do
    def part1(path) do
        File.read!(path)
        |> String.split("\r\n")
        |> Enum.filter(fn s -> s != "" end)
        |> Enum.map(&String.to_integer/1)
        |> Enum.sum()
    end

    def part2(path) do
        File.read!(path)
        |> String.split("\r\n")
        |> Enum.filter(fn s -> s != "" end)
        |> Enum.map(&String.to_integer/1)
        |> get_duplicate_freq()
    end

    def get_duplicate_freq(list) do
        size = length(list)
        index = 0
        seen = MapSet.new([0])
        [current | _] = list
        do_get_duplicate_freq(list, size, index, seen, current)
    end

    defp do_get_duplicate_freq(list, size, index, seen, current) do
        if MapSet.member?(seen, current) do
            current
        else
            seen = MapSet.put(seen, current)
            index = next_index(index, size)
            current = current + Enum.at(list, index)
            do_get_duplicate_freq(list, size, index, seen, current)
        end
    end

    defp next_index(index, size), do: (index + 1) |> rem(size)
end

path = "../inputs/day1.txt"
IO.puts Day1.part1(path)
IO.puts Day1.part2(path)