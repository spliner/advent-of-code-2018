# TODO: actually get better at this

defmodule Day2 do
    def part1(path) do
        File.read!(path)
        |> String.split("\r\n")
        |> Enum.filter(fn s -> s != "" end)
        |> Enum.map(&String.graphemes/1)
        |> Enum.map(&group_by_count/1)
        |> Enum.map(fn g -> {get_count(g, 2), get_count(g, 3)} end)
        |> Enum.reduce(fn {x, y}, {twos, threes} -> {twos + x, threes + y} end)
        |> multiply_tuple()
        |> IO.inspect()
    end

    defp group_by_count(xs) do
        Enum.group_by(xs, fn x -> Enum.count(xs, fn y -> x == y end) end)
    end

    defp get_count(map, key) do
        case map[key] do
            nil -> 0
            _ -> 1
        end
    end

    defp multiply_tuple({x, y}), do: x * y
end

path = "../inputs/day2.txt"
Day2.part1(path)