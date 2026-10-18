export default function Tag({ label }: { label: string }) {
  return (
    <span className="inline-block px-2.5 py-0.5 rounded-full text-xs border border-zinc-700 bg-zinc-900 text-zinc-300">
      {label.replace(/_/g, " ")}
    </span>
  );
}
